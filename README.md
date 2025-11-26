pyKRC
==================

A Python REST API client for Kitten Space Agency (KSA) remote control.

See the [repository](https://github.com/MarcusZuber/pyKRC) for more information.
This requires the running Kitten Space Agency server with the KittenRemoteControl mod, which can be
found [here](https://github.com/MarcusZuber/KittenRemoteControl).

The library uses a RESTful API to communicate with the KSA server.

Installation
-------------

```bash
pip install .
```

Usage
-----

### Testing the Connection

To test your connection, run:

```bash
pyKRC_info --address localhost --port 8080
```

If you do not run a server locally, replace `localhost` with the server address.
If it works, it should print out information about the package and telemetry data from the server.

### Basic Example

Here is a simple example of how to use the library:

```python
from time import sleep
from pyKRC import Control, Telemetry

# Initialize control and telemetry clients
control = Control("localhost", 8080)
telemetry = Telemetry("localhost", 8080)

# Get telemetry data
print(f"Altitude: {telemetry.altitude} m")
print(f"Apoapsis: {telemetry.apoapsis} m")
print(f"Periapsis: {telemetry.periapsis} m")

# Control the spacecraft
control.throttle = 0.5  # Set throttle to 50%
control.start_engine()
sleep(10)
control.stop_engine()
```

### Control Features

```python
from pyKRC import Control

control = Control("localhost", 8080)

# Throttle control (0.0 to 1.0)
control.throttle = 0.75
current_throttle = control.throttle

# Engine control
control.start_engine()
control.stop_engine()
# Or use the property
control.engine_on = True

# Reference frame
control.reference_frame = "LVLH"
frames = control.get_reference_frames()

# Flight computer
control.attitude_mode = "Auto"
modes = control.get_attitude_modes()
control.set_stabilization(True)
```

### Telemetry Features

```python
from pyKRC import Telemetry

telemetry = Telemetry("localhost", 8080)

# Orbital parameters
print(f"Apoapsis: {telemetry.apoapsis} m")
print(f"Periapsis: {telemetry.periapsis} m")
print(f"Apoapsis Elevation: {telemetry.apoapsis_elevation} m")
print(f"Periapsis Elevation: {telemetry.periapsis_elevation} m")

# Speed and mass
print(f"Orbital Speed: {telemetry.orbital_speed} m/s")
print(f"Propellant Mass: {telemetry.propellant_mass} kg")
print(f"Total Mass: {telemetry.total_mass} kg")

# Celestial body info
print(f"Mean Radius: {telemetry.mean_radius} m")
```

### Command Line Interface

A simple CLI tool is included:

```bash
# Get values
python remote_control_client.py get throttle
python remote_control_client.py get apoapsis

# Set values
python remote_control_client.py set throttle 0.75
python remote_control_client.py set engine_on true

# List available options
python remote_control_client.py list reference_frames
python remote_control_client.py list attitude_modes
```

API Reference
-------------

### Control Class

- `throttle` (property): Get/set engine throttle (0.0 to 1.0)
- `engine_on` (property): Get/set engine state (bool)
- `start_engine()`: Turn engine on
- `stop_engine()`: Turn engine off
- `reference_frame` (property): Get/set reference frame (string or int)
- `get_reference_frames()`: List all available reference frames
- `attitude_mode` (property): Get/set flight computer attitude mode
- `get_attitude_modes()`: List all available attitude modes
- `set_stabilization(enabled)`: Enable/disable stabilization

### Telemetry Class

- `altitude`: Current altitude (m)
- `apoapsis`: Apoapsis of current orbit (m)
- `periapsis`: Periapsis of current orbit (m)
- `apoapsis_elevation`: Apoapsis above surface (m)
- `periapsis_elevation`: Periapsis above surface (m)
- `orbital_speed`: Current orbital speed (m/s)
- `propellant_mass`: Current propellant mass (kg)
- `total_mass`: Total vessel mass (kg)
- `mean_radius`: Mean radius of orbited body (m)

Error Handling
--------------

The library uses standard Python exceptions:

```python
import requests
from pyKRC import Control

control = Control("localhost", 8080)

try:
    control.throttle = 0.5
except requests.exceptions.ConnectionError:
    print("Could not connect to server")
except RuntimeError as e:
    print(f"Server error: {e}")
```

