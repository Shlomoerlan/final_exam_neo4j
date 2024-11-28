from app.repository.crud_relation_neo4j import create_relationship
from toolz import get

def create_relation_interaction(data):
    start_id, end_id = get([0, 1], data['devices'])["id"]
    properties = get('interaction', data)
    res = create_relationship(
        "DeviceLocation",
        start_id, "DeviceLocation",
        end_id,
        "CONNECTED",
        properties
    )
    return res