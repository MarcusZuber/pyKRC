"""
Simple Python client for KittenRemoteControl RESTful API

Usage:
    python remote_control_client.py get throttle
    python remote_control_client.py set throttle 0.75
    python remote_control_client.py get apoapsis
    python remote_control_client.py set engine_on true
"""

import sys
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
            print("                 apoapsis, periapsis, apoapsis_elevation, periapsis_elevation,")
            print("                 orbital_speed, propellant_mass, total_mass, mean_radius")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


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
        else:
            print(f"Unknown or read-only path: {path}")
            print("Available writable paths: throttle, engine_on, reference_frame, attitude_mode, stabilization")
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
        value = sys.argv[3]
        set_value(path, value)
    elif verb == "list" and len(sys.argv) >= 3:
        path = sys.argv[2]
        list_values(path)
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()

