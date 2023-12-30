# PyGradient - API server for AirGradient devices

PyGradient runs a local HTTP server for accepting data from AirGradient sensors running stock firmware.

## Supported sensors

- AirGradient ONE V9 (ONE-V9)
- AirGradient Outdoor Monitor with dual PM sensors (O-1PP)


*Device data is matched against the schemas defined in [pygradient/models.py](./pygradient/models.py).*

## Installation
PyGradient can be installed directly from GitHub using pip:

`pip install git+https://github.com/just-oblivious/pygradient.git`

Python 3.11 or newer is required.

## Device preparation

AirGradient devices post data to a hardcoded HTTP endpoint (`hw.airgradient.com`), this URL needs to be modified to make the sensor talk to a local endpoint:

1. Setup a development environment as per  [AirGradients instructions](https://www.airgradient.com/blog/install-arduino-c3-mini/);
1. Open the Arduino code for your AirGradient device;
1. Patch the `APIROOT` variable and point it to your local machine (e.g. `http://192.168.1.10:8088/`);
1. Flash the firmware to your device;
1. Run `python3 -m pygradient` and watch the data arrive. The default port for PyGradient is `8088`.

## Basic example
```python
from pygradient import SensorAPI, SensorData


# This callback function is called upon receiving a valid measurement.
def sensor_callback(sensor_data: SensorData) -> None:
    """This is where you'd do something useful with the readings."""
    print(f"Sensor ID: {sensor_data.id} ({sensor_data.ip})")
    for key, value in sensor_data.readings:
        print(f"{key}: {value}")


api = SensorAPI()

# Register the callback function
api.register_callback(sensor_callback)

# Run the API server
api.serve("0.0.0.0", 8088)

```

Example output:
```
Sensor ID: 1337b00cface (10.0.0.142)
pm01: 1
pm02: 2
pm10: 2
pm003_count: 420
atmp: 22.25
rhum: 43
wifi: -38
boot: 1302
sensor_model: ONE-V9
rco2: 796
tvoc_index: 81
nox_index: 1
```

## Async example

```python
import asyncio

from pygradient import SensorAPI, SensorData


# This callback function is called upon receiving a valid measurement.
async def sensor_callback(sensor_data: SensorData) -> None:
    """This is where you'd do something useful with the readings."""
    print(f"Sensor ID: {sensor_data.id} ({sensor_data.ip})")
    for key, value in sensor_data.readings:
        print(f"{key}: {value}")


api = SensorAPI()

api.register_async_callback(sensor_callback)


async def main() -> None:
    # Start serving the API endpoint
    await api.async_serve()

    # Do something else
    await asyncio.sleep(30)

    # Stop serving the API endpoint
    await api.async_teardown()


asyncio.run(main())

```
