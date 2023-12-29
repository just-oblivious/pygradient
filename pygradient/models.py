from typing import Dict, List, Optional, Union

from pydantic import BaseModel, StrictStr, validator


class AG(BaseModel):
    """WiFi RSSI and loop count."""

    wifi: int
    boot: int


class PMTH(BaseModel):
    """Particulate matter, temperature, and humidity readings."""

    pm01: int
    pm02: int
    pm10: int
    pm003_count: int
    atmp: int | float
    rhum: int | float


class ONEV9Reading(AG, PMTH):
    """Sensor readings supported by the ONE V9."""

    sensor_model: str = "ONE-V9"
    rco2: int
    tvoc_index: int
    nox_index: int


class OutdoorPPReading(AG, PMTH):
    """Sensor readings supported by the Outdoor Monitor with dual PM channels."""

    sensor_model: str = "O-1PP"
    channels: List[PMTH]

    @validator("channels", pre=True)
    def init_channels(cls, obj: Dict[str, Dict[str, int | float]]) -> List[PMTH]:
        return [PMTH.model_validate(obj["1"]), PMTH.model_validate(obj["2"])]


class SensorData(BaseModel):
    """Data from an AirGradient sensor."""

    id: StrictStr
    ip: Optional[str]
    readings: Union[
        ONEV9Reading,
        OutdoorPPReading,
    ]
