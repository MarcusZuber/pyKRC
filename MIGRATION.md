# Migration Guide: Socket API to RESTful API

This guide helps you migrate from pyKRC 0.1.x (Socket-based) to 0.2.x (RESTful API).

## Overview of Changes

The main change is that pyKRC now communicates with the KSA server using a RESTful API with JSON responses instead of a custom socket protocol with text responses.

## What Stays the Same

- Initialization of `Control` and `Telemetry` classes
- Most property names and method signatures
- Basic usage patterns

## Breaking Changes

### 1. Server Requirements

**Old**: Required KittenRemoteControl mod with socket server
**New**: Requires KittenRemoteControl mod with RESTful API server

Make sure your KittenRemoteControl mod is updated to version 1.0.0 or later.

### 2. Response Format

The internal `_get()` and `_set()` methods now return JSON objects instead of plain text strings.

**Impact**: Only affects you if you were using internal methods directly. Public API remains mostly the same.

## Code Migration Examples

### Basic Usage (No Changes Needed)

```python
# This code works in both 0.1.x and 0.2.x
from pyKRC import Control, Telemetry

control = Control("localhost", 8080)
telemetry = Telemetry("localhost", 8080)

# These work the same
control.throttle = 0.5
control.start_engine()
control.stop_engine()
print(telemetry.apoapsis)
print(telemetry.periapsis)
```

### Throttle Values

**Old (0.1.x)**: Throttle was documented as 0-100 but actually expected 0.0-1.0
**New (0.2.x)**: Throttle is consistently 0.0-1.0

```python
# Old code that might have been confusing
control.throttle = 75  # Was this 75% or invalid?

# New code - always use 0.0 to 1.0
control.throttle = 0.75  # Clearly 75%
```

### Engine Control Enhancement

**New in 0.2.x**: You can now use a boolean property for engine state:

```python
# Old way (still works)
control.start_engine()
control.stop_engine()

# New way (recommended)
control.engine_on = True
control.engine_on = False

# You can also check the state
if control.engine_on:
    print("Engine is running")
```

### Error Handling

**Old (0.1.x)**: Raised generic `ConnectionError` or `RuntimeError`
**New (0.2.x)**: Uses `requests.exceptions.ConnectionError` for connection issues

```python
# Old error handling
try:
    control.throttle = 0.5
except ConnectionError:
    print("Connection failed")

# New error handling (recommended)
import requests

try:
    control.throttle = 0.5
except requests.exceptions.ConnectionError:
    print("Connection failed")
except RuntimeError as e:
    print(f"Server error: {e}")
```

## New Features in 0.2.x

Take advantage of these new features:

### Additional Telemetry

```python
from pyKRC import Telemetry

telemetry = Telemetry("localhost", 8080)

# New properties available
print(f"Apoapsis Elevation: {telemetry.apoapsis_elevation} m")
print(f"Periapsis Elevation: {telemetry.periapsis_elevation} m")
print(f"Orbital Speed: {telemetry.orbital_speed} m/s")
print(f"Propellant Mass: {telemetry.propellant_mass} kg")
print(f"Total Mass: {telemetry.total_mass} kg")
print(f"Mean Radius: {telemetry.mean_radius} m")
```

### Reference Frame Control

```python
from pyKRC import Control

control = Control("localhost", 8080)

# Get/set reference frame
current_frame = control.reference_frame
control.reference_frame = "LVLH"

# List available frames
frames = control.get_reference_frames()
for frame in frames:
    print(f"{frame['name']}: {frame['value']}")
```

### Flight Computer Control

```python
from pyKRC import Control

control = Control("localhost", 8080)

# Attitude mode control
current_mode = control.attitude_mode
control.attitude_mode = "Auto"

# List available modes
modes = control.get_attitude_modes()

# Stabilization
control.set_stabilization(True)
```

## Testing Your Migration

1. Update your KittenRemoteControl mod to the latest version
2. Update pyKRC: `pip install --upgrade .`
3. Run your existing code - most should work without changes
4. Update error handling to use `requests.exceptions.ConnectionError`
5. Consider using new features like `control.engine_on` property
6. Test with the included `remote_control_client.py` or `example_usage.py`

## Troubleshooting

### "Connection refused" errors

**Cause**: The server might still be using the old socket protocol.
**Solution**: Update your KittenRemoteControl mod to the newest version.

### "KeyError" when accessing values

**Cause**: You might be using internal `_get()` or `_set()` methods directly.
**Solution**: Use the public properties and methods instead.

### Throttle not working as expected

**Cause**: You might be passing values > 1.0
**Solution**: Use values between 0.0 and 1.0 (e.g., 0.75 for 75%)

## Need Help?

If you encounter issues during migration:
1. Check the [README.md](README.md) for usage examples
2. Review the [CHANGELOG.md](CHANGELOG.md) for detailed changes
3. Open an issue on GitHub with your specific problem

