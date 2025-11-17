pyKRC
==================

A small REST API client to access kitten space agency.

See the [repository](https://github.com/MarcusZuber/pyKRC) for more information.
This requires the running kitten space agency server remote control server, which can be
found [here](https://github.com/MarcusZuber/KittenRemoteControl).

Installation
-------------


```bash
pip install .
```

Usage
-----

To test, you can run this command:

```bash
pyKRC_info --host localhost --port 8080
```

If you do not run a server locally, replace `localhost` with the server address.
If it works, it should print out some information about the connected server.


Here is a small example of how to use the library:
```python
from time import sleep
from pyKRC import Control, Telemetry

control = Control("localhost", 8080)
telemetry = Telemetry("localhost", 8080)

print(telemetry.altitude)
control.throttle = 50
control.start_engine()
sleep(10)
control.stop_engine()
```

