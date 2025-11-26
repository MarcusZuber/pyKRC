"""
Example usage of pyKRC with the RESTful API

This script demonstrates how to use the pyKRC library to:
- Get and set throttle
- Control engine state
- Get telemetry data
- Manage reference frames and flight computer settings
"""

from pyKRC import Control, Telemetry


def main():
    # Initialize control and telemetry
    control = Control(address="localhost", port=8080)
    telemetry = Telemetry(address="localhost", port=8080)

    try:
        # === Throttle Control ===
        print("=== Throttle Control ===")
        current_throttle = control.throttle
        print(f"Current throttle: {current_throttle}")

        # Set throttle to 50%
        control.throttle = 0.5
        print(f"Throttle set to: {control.throttle}")

        # === Engine Control ===
        print("\n=== Engine Control ===")
        engine_state = control.engine_on
        print(f"Engine is: {'ON' if engine_state else 'OFF'}")

        # Turn engine on
        control.start_engine()
        print("Engine started")

        # Or use property
        # control.engine_on = True

        # === Telemetry Data ===
        print("\n=== Telemetry Data ===")
        print(f"Apoapsis: {telemetry.apoapsis:.2f} m")
        print(f"Periapsis: {telemetry.periapsis:.2f} m")
        print(f"Apoapsis Elevation: {telemetry.apoapsis_elevation:.2f} m")
        print(f"Periapsis Elevation: {telemetry.periapsis_elevation:.2f} m")
        print(f"Orbital Speed: {telemetry.orbital_speed:.2f} m/s")
        print(f"Propellant Mass: {telemetry.propellant_mass:.2f} kg")
        print(f"Total Mass: {telemetry.total_mass:.2f} kg")
        print(f"Mean Radius: {telemetry.mean_radius:.2f} m")

        # === Reference Frame ===
        print("\n=== Reference Frame ===")
        current_frame = control.reference_frame
        print(f"Current reference frame: {current_frame}")

        # Get all available frames
        frames = control.get_reference_frames()
        print("Available reference frames:")
        for frame in frames:
            print(f"  - {frame['name']} (ID: {frame['value']})")

        # Set reference frame by name
        # control.reference_frame = "LVLH"

        # === Flight Computer ===
        print("\n=== Flight Computer ===")
        current_mode = control.attitude_mode
        print(f"Current attitude mode: {current_mode}")

        # Get all available modes
        modes = control.get_attitude_modes()
        print("Available attitude modes:")
        for mode in modes:
            print(f"  - {mode['name']} (ID: {mode['value']})")

        # Set attitude mode
        # control.attitude_mode = "Auto"

        # Enable stabilization
        # control.set_stabilization(True)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

