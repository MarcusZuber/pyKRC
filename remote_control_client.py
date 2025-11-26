"""
Simple Python client for KittenRemoteControl RESTful API

Usage:
    python remote_control_client.py get throttle
    python remote_control_client.py set throttle 0.75
    python remote_control_client.py get apoapsis
    python remote_control_client.py set engine_on true
    python remote_control_client.py get thrusters
    python remote_control_client.py set thrusters '{"RollRight": true, "PitchUp": false}'
"""

import sys
import json
import ast
import re
from pyKRC import Control, Telemetry


HOST = "localhost"
PORT = 8080


def get_value(path: str):
    """Get a value from the server"""
    control = Control(address=HOST, port=PORT)
    telemetry = Telemetry(address=HOST, port=PORT)

    try:
        if path == "throttle":
            value = control.throttle
            print(f"Throttle: {value}")
        elif path == "engine_on":
            value = control.engine_on
            print(f"Engine On: {value}")
        elif path == "reference_frame":
            value = control.reference_frame
            print(f"Reference Frame: {value}")
        elif path == "attitude_mode":
            value = control.attitude_mode
            print(f"Attitude Mode: {value}")
        elif path == "thrusters":
            mapping = control.get_thrusters()
            print("Thrusters:")
            for k, v in mapping.items():
                print(f"  {k}: {v}")
        elif path == "apoapsis":
            value = telemetry.apoapsis
            print(f"Apoapsis: {value} m")
        elif path == "periapsis":
            value = telemetry.periapsis
            print(f"Periapsis: {value} m")
        elif path == "apoapsis_elevation":
            value = telemetry.apoapsis_elevation
            print(f"Apoapsis Elevation: {value} m")
        elif path == "periapsis_elevation":
            value = telemetry.periapsis_elevation
            print(f"Periapsis Elevation: {value} m")
        elif path == "orbital_speed":
            value = telemetry.orbital_speed
            print(f"Orbital Speed: {value} m/s")
        elif path == "propellant_mass":
            value = telemetry.propellant_mass
            print(f"Propellant Mass: {value} kg")
        elif path == "total_mass":
            value = telemetry.total_mass
            print(f"Total Mass: {value} kg")
        elif path == "mean_radius":
            value = telemetry.mean_radius
            print(f"Mean Radius: {value} m")
        else:
            print(f"Unknown path: {path}")
            print("Available paths: throttle, engine_on, reference_frame, attitude_mode,")
            print("                 thrusters, apoapsis, periapsis, apoapsis_elevation, periapsis_elevation,")
            print("                 orbital_speed, propellant_mass, total_mass, mean_radius")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def parse_thrusters_arg(arg: str) -> dict:
    """
    Parse thrusters set argument.
    Accepts JSON string like '{"RollRight": true}' or comma-separated key=value pairs 'RollRight=1,PitchUp=0'.
    Values '1', 'true', 'True' -> True; '0','false','False' -> False.
    """
    s = arg.strip()
    # Strip matching outer quotes (single or double) if present — shells often pass quoted strings
    if len(s) >= 2 and ((s[0] == s[-1]) and s[0] in "'\""):
        s_inner = s[1:-1].strip()
    else:
        s_inner = s

    # If enclosed in braces, remove them for fallback parsing: {a:1, b:0} -> a:1, b:0
    if len(s_inner) >= 2 and s_inner[0] == '{' and s_inner[-1] == '}':
        s_inner_braceless = s_inner[1:-1].strip()
    else:
        s_inner_braceless = s_inner

    # Try JSON first
    try:
        parsed = json.loads(s_inner)
        if isinstance(parsed, dict):
            # If nested under 'thrusters', return inner mapping
            return parsed.get('thrusters', parsed)
    except Exception:
        pass

    # Try Python literal (accepts single quotes, True/False)
    try:
        # convert JSON-style true/false into Python True/False for literal_eval
        s_py = re.sub(r'\btrue\b', 'True', s_inner, flags=re.IGNORECASE)
        s_py = re.sub(r'\bfalse\b', 'False', s_py, flags=re.IGNORECASE)
        parsed = ast.literal_eval(s_py)
        if isinstance(parsed, dict):
            return parsed.get('thrusters', parsed)
    except Exception:
        pass

    # Fallback: parse key=value pairs or key: value pairs
    result = {}
    pairs = [p.strip() for p in s_inner_braceless.split(',') if p.strip()]
    for p in pairs:
        # accept either key=value or key: value
        sep = '=' if '=' in p else ':' if ':' in p else None
        if sep is None:
            raise ValueError(f"Invalid thruster pair: {p}")
        k, v = p.split(sep, 1)
        v = v.strip()
        if v.lower() in ['1', 'true', 'yes', 'on']:
            result[k.strip()] = True
        elif v.lower() in ['0', 'false', 'no', 'off']:
            result[k.strip()] = False
        else:
            # try numeric
            try:
                num = float(v)
                result[k.strip()] = bool(num)
            except Exception:
                # keep as string
                result[k.strip()] = v
    return result


def set_value(path: str, value: str):
    """Set a value on the server"""
    control = Control(address=HOST, port=PORT)

    try:
        if path == "throttle":
            control.throttle = float(value)
            print(f"Successfully set throttle to {value}")
        elif path == "engine_on":
            bool_value = value.lower() in ['true', '1', 'yes', 'on']
            control.engine_on = bool_value
            print(f"Successfully set engine_on to {bool_value}")
        elif path == "reference_frame":
            control.reference_frame = value
            print(f"Successfully set reference_frame to {value}")
        elif path == "attitude_mode":
            control.attitude_mode = value
            print(f"Successfully set attitude_mode to {value}")
        elif path == "stabilization":
            bool_value = value.lower() in ['true', '1', 'yes', 'on']
            control.set_stabilization(bool_value)
            print(f"Successfully set stabilization to {bool_value}")
        elif path == "thrusters":
            thr_map = parse_thrusters_arg(value)
            updated = control.set_thrusters(thr_map)
            print("Successfully updated thrusters:")
            for k, v in updated.items():
                print(f"  {k}: {v}")
        else:
            print(f"Unknown or read-only path: {path}")
            print("Available writable paths: throttle, engine_on, reference_frame, attitude_mode, stabilization, thrusters")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def list_values(path: str):
    """List available options"""
    control = Control(address=HOST, port=PORT)

    try:
        if path == "reference_frames":
            frames = control.get_reference_frames()
            print("Available reference frames:")
            for frame in frames:
                print(f"  - {frame['name']} (ID: {frame['value']})")
        elif path == "attitude_modes":
            modes = control.get_attitude_modes()
            print("Available attitude modes:")
            for mode in modes:
                print(f"  - {mode['name']} (ID: {mode['value']})")
        else:
            print(f"Unknown list path: {path}")
            print("Available list paths: reference_frames, attitude_modes")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    verb = sys.argv[1].lower()

    if verb == "get" and len(sys.argv) >= 3:
        path = sys.argv[2]
        get_value(path)
    elif verb == "set" and len(sys.argv) >= 4:
        path = sys.argv[2]
        # Join remaining args for thrusters JSON/kv parsing
        value = ' '.join(sys.argv[3:])
        set_value(path, value)
    elif verb == "list" and len(sys.argv) >= 3:
        path = sys.argv[2]
        list_values(path)
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
