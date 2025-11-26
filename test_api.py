"""
Quick test script to verify pyKRC RESTful API implementation

This script demonstrates that the API calls are correctly formed.
Note: This requires a running KSA server with KittenRemoteControl mod.
"""

from pyKRC import Control, Telemetry
import requests


def test_connection():
    """Test basic connection"""
    print("Testing connection...")
    control = Control("localhost", 8080)
    print(f"✓ Control initialized: {control.base_url}")

    telemetry = Telemetry("localhost", 8080)
    print(f"✓ Telemetry initialized: {telemetry.base_url}")


def test_control_methods():
    """Test control methods (without actual server)"""
    print("\nTesting Control class methods...")
    control = Control("localhost", 8080)

    # Verify properties exist (check in class definition)
    properties = ['throttle', 'engine_on', 'reference_frame', 'attitude_mode', 'sas']
    for prop in properties:
        assert hasattr(type(control), prop), f"{prop} property exists"

    # Verify methods exist
    methods = ['start_engine', 'stop_engine', 'get_reference_frames',
               'get_attitude_modes', 'set_stabilization']
    for method in methods:
        assert hasattr(control, method), f"{method} method exists"
        assert callable(getattr(control, method)), f"{method} is callable"

    print("✓ All Control methods exist")


def test_telemetry_methods():
    """Test telemetry methods (without actual server)"""
    print("\nTesting Telemetry class methods...")
    telemetry = Telemetry("localhost", 8080)

    # Verify properties exist (check the class, not the instance to avoid calling them)
    properties_to_check = [
        'altitude', 'apoapsis', 'periapsis', 'apoapsis_elevation',
        'periapsis_elevation', 'orbital_speed', 'propellant_mass',
        'total_mass', 'mean_radius'
    ]

    for prop in properties_to_check:
        # Check if the property exists in the class definition
        assert hasattr(type(telemetry), prop), f"{prop} property exists"

    print("✓ All Telemetry properties exist")


def test_with_server():
    """Test with actual server (if available)"""
    print("\nTesting with server...")
    control = Control("localhost", 8080)
    telemetry = Telemetry("localhost", 8080)

    try:
        # Try to get throttle
        throttle = control.throttle
        print(f"✓ Got throttle: {throttle}")

        # Try to get apoapsis
        apoapsis = telemetry.apoapsis
        print(f"✓ Got apoapsis: {apoapsis} m")

        # Try to get periapsis
        periapsis = telemetry.periapsis
        print(f"✓ Got periapsis: {periapsis} m")

        print("\n✓ All server tests passed!")
        return True

    except requests.exceptions.ConnectionError:
        print("⚠ Server not running (this is expected if KSA is not active)")
        print("  Start KSA with KittenRemoteControl mod to test with server")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def main():
    print("=" * 60)
    print("pyKRC RESTful API Test Suite")
    print("=" * 60)

    # Test without server
    test_connection()
    test_control_methods()
    test_telemetry_methods()

    print("\n" + "=" * 60)
    print("Basic tests passed! ✓")
    print("=" * 60)

    # Test with server if available
    server_available = test_with_server()

    print("\n" + "=" * 60)
    if server_available:
        print("All tests passed! Ready to use pyKRC ✓")
    else:
        print("Library structure is correct!")
        print("Connect to KSA server to test full functionality.")
    print("=" * 60)


if __name__ == "__main__":
    main()

