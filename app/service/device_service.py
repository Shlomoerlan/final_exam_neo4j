from typing import List
from returns.result import Success, Failure, Result
from app.db.models import DeviceLocation
from app.repository.crud_neo4j import insert_object, update_object
from app.utills.functions_utills import check_device_exists


def create_device(device_location: DeviceLocation)->Result[DeviceLocation, str]:
    try:
        res = insert_object(device_location)
        return Success(res)
    except Exception as e:
        return Failure(str(e))

def update_device(device_location: DeviceLocation)->Result[DeviceLocation, str]:
    try:
        res = update_object(device_location, device_location.id)
        return Success(res)
    except Exception as e:
        return Failure(str(e))

def upsert_device(device_locations: List[DeviceLocation])->List:
    if any(map(lambda pair: pair[0].device_id == pair[1].device_id, zip(device_locations, device_locations[1:]))):
        raise Exception("cannot upsert same device")
    for device_location in device_locations:
        is_exist = check_device_exists(device_location.device_id)
        if not is_exist:
            res = create_device(device_location)
            yield res
        res = update_device(device_location)
        yield res

def handle_upsert(devices):
    try:
        return list(upsert_device(devices))
    except Exception as e:
        return f"Error: {e}"