from dataclasses import dataclass

@dataclass
class Device:
    device_id: str
    name: str
    brand: str
    model: str
    os: str