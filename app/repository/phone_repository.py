from app.db.database import driver

def count_connected_devices(device_id: str) -> int:
    query = """
    MATCH (:DeviceLocation {device_id: $device_id})-[:CONNECTED]->(connected:DeviceLocation)
    RETURN count(connected) AS connected_count
    """
    with driver.session() as session:
        result = session.run(query, {"device_id": device_id})
        record = result.single()
        if record:
            return record["connected_count"]
        return 0

def is_connected(device_id_1: str, device_id_2: str) -> bool:
    query = """
    MATCH (a:DeviceLocation {device_id: $device_id_1})-[:CONNECTED]-(b:DeviceLocation {device_id: $device_id_2})
    RETURN count(*) > 0 AS is_connected
    """
    with driver.session() as session:
        result = session.run(query, {"device_id_1": device_id_1, "device_id_2": device_id_2})
        record = result.single()
        return record["is_connected"] if record else False

def fetch_most_recent_interaction(device_id: str) -> dict:
    query = """
    MATCH (a:DeviceLocation {device_id: $device_id})-[r:CONNECTED]-(b:DeviceLocation)
    RETURN r, b
    ORDER BY r.timestamp DESC
    LIMIT 1
    """
    with driver.session() as session:
        result = session.run(query, {"device_id": device_id})
        record = result.single()
        if record:
            return {
                "interaction": dict(record["r"]),
                "connected_device": dict(record["b"])
            }
        return None


def find_bluetooth_connections():
    with driver.session() as session:
        query = """
        MATCH path = (d1:DeviceLocation)-[r:CONNECTED*]->(d2:DeviceLocation)
        WHERE all(rel IN r WHERE rel.method = 'Bluetooth')
        RETURN 
            d1.device_id AS from_device, 
            d2.device_id AS to_device, 
            length(path) AS path_length
        ORDER BY length(path) DESC
        LIMIT 1
        """
        result = session.run(query)
        return [
            {
                "from_device": record["from_device"],
                "to_device": record["to_device"],
                "path_length": record["path_length"]
            } for record in result
        ]

def find_strong_signal_connections():
    with driver.session() as session:
        query = """
        MATCH path = (d1:DeviceLocation)-[r:CONNECTED]->(d2:DeviceLocation)
        WHERE r.signal_strength_dbm > -60
        RETURN
            d1.device_id AS from_device,
            d2.device_id AS to_device,
            r.signal_strength_dbm AS signal_strength
        """
        result = session.run(query)
        return [
            {
                "from_device": record["from_device"],
                "to_device": record["to_device"],
                "signal_strength": record["signal_strength"]
            } for record in result
        ]

def count_device_connections(device_id):
    with driver.session() as session:
        query = """
        MATCH (d:DeviceLocation {id: $device_id})-[r:CONNECTED]->()
        RETURN count(r) AS connection_count
        """
        result = session.run(query, {"device_id": device_id}).single()
        return result["connection_count"] if result else 0
