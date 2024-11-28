from dataclasses import dataclass

@dataclass
class DeviceLocation:
    device_id: str
    name: str
    brand: str
    model: str
    os: str
    latitude: float
    longitude: float
    altitude_meters: int
    accuracy_meters: int