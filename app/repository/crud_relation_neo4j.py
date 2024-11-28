from app.db.database import driver


def create_relationship(start_type, start_id, end_type, end_id, relationship_type, relationship_properties=None):
    with driver.session() as session:
        params = {"start_id": start_id, "end_id": end_id}
        query = (
            f"MATCH (a:{start_type}), (b:{end_type}) "
            f"WHERE a.device_id = $start_id AND b.device_id = $end_id "
            f"MERGE (a)-[r:{relationship_type} {{ {', '.join([f'{k}: ${k}' for k in relationship_properties.keys()])} }}]->(b) "
            f"RETURN r"
        )
        running_params = params if not relationship_properties else { **params, **relationship_properties}
        res = session.run(query, running_params     ).data()
        return res

