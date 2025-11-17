import argparse

import requests

from . import __version__, Telemetry


def build_info() -> dict:
    return {
        "name": "pyKRC",
        "version": __version__,
    }


def build_telemetry_info(address: str, port: int) -> dict:
    telemetry = Telemetry(address=address, port=port)
    return {"altitude": telemetry.altitude, "apoapsis": telemetry.apoapsis, "periapsis": telemetry.periapsis}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="pyKRC_info", description="Show pyKRC package info")

    parser.add_argument("--address", "-a", default="localhost", help="Address to use (default: localhost)")
    parser.add_argument("--port", "-p", type=int, default=8080, help="Port to use (default: 8080)")
    args = parser.parse_args(argv)

    info = build_info()
    print(f"pyKRC {info['version']}")
    print(f"Name: {info['name']}")
    print(f"Address: {args.address}")
    print(f"Port: {args.port}")

    try:
        telemetry = build_telemetry_info(args.address, args.port)
        print("Telemetry")
        print(f"  Altitude: {telemetry['altitude']} m")
        print(f"  Apoapsis: {telemetry['apoapsis']} m")
        print(f"  Periapsis: {telemetry['periapsis']} m")
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to the KSA server")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
