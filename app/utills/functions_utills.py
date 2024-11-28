from app.db.database import driver
from app.db.models import DeviceLocation, Interaction
from datetime import datetime
from typing import List, Tuple

def check_device_exists(device_id):
    with driver.session() as session:
        query = """
        MATCH (d:Device {id: $device_id})
        RETURN count(d) > 0 AS exists
        """
        params = {"device_id": device_id}
        result = session.run(query, params)
        return result.single()["exists"]

def create_device_location_model(device: dict) -> DeviceLocation:
    return DeviceLocation(
            device_id=device["id"],
            name=device["name"],
            brand=device["brand"],
            model=device["model"],
            os=device["os"],
            latitude=device["location"]["latitude"],
            longitude=device["location"]["longitude"],
            altitude_meters=device["location"]["altitude_meters"],
            accuracy_meters=device["location"]["accuracy_meters"]
    )

def create_interaction_model(interaction_data: dict) -> Interaction:
    return Interaction(
        from_device=interaction_data["from_device"],
        to_device=interaction_data["to_device"],
        method=interaction_data["method"],
        bluetooth_version=interaction_data["bluetooth_version"],
        signal_strength_dbm=interaction_data["signal_strength_dbm"],
        distance_meters=interaction_data["distance_meters"],
        duration_seconds=interaction_data["duration_seconds"],
        timestamp=datetime.fromisoformat(interaction_data["timestamp"])
    )

def get_models_from_data(data: dict) -> Tuple[List[DeviceLocation], Interaction]:
    devices = [
        create_device_location_model(device)
        for device in data["devices"]
    ]
    interaction_data = data["interaction"]
    interaction = create_interaction_model(interaction_data)
    return devices, interaction