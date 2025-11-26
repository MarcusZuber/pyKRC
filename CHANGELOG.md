# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] - 2025-11-26

### Changed
- **BREAKING**: Migrated from Socket-based communication to RESTful API
  - `connection.py` now uses `requests` library instead of raw sockets
  - All responses are now JSON objects instead of plain text
  - API endpoints now use HTTP GET/PUT methods instead of "GET"/"SET" commands

### Added
- New telemetry properties:
  - `apoapsis_elevation`: Apoapsis elevation above surface
  - `periapsis_elevation`: Periapsis elevation above surface
  - `orbital_speed`: Current orbital speed in m/s
  - `propellant_mass`: Current propellant mass in kg
  - `total_mass`: Total vessel mass in kg
  - `mean_radius`: Mean radius of the body being orbited
  
- New control features:
  - `engine_on` property: Get/set engine state as boolean
  - `reference_frame` property: Get/set reference frame
  - `get_reference_frames()`: List all available reference frames
  - `attitude_mode` property: Get/set flight computer attitude mode
  - `get_attitude_modes()`: List all available attitude modes
  - `set_stabilization(enabled)`: Enable/disable spacecraft stabilization

- New example files:
  - `example_usage.py`: Comprehensive usage examples
  - `remote_control_client.py`: CLI tool for controlling KSA

### Fixed
- Improved error handling with proper exception types
- Better timeout handling (5 second default)
- Connection errors now properly raise `requests.exceptions.ConnectionError`

### Documentation
- Updated README with comprehensive examples
- Added API reference section
- Added error handling examples
- Documented all new features

## [0.1.0] - Initial Release

### Added
- Basic socket-based communication with KSA server
- `Control` class for spacecraft control
- `Telemetry` class for reading telemetry data
- Basic throttle and engine control
- Apoapsis and periapsis telemetry

