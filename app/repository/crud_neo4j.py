from operator import itemgetter
from returns.maybe import Maybe
from app.db.database import driver
from dataclasses import asdict


def insert_object(T, R=None):
    with driver.session() as session:
        model = asdict(T)
        if R:
            model.update(R)
        model_type = type(T).__name__
        fields = ", ".join([f"{k}: ${k}" for k in model.keys()])
        query = f"MERGE (t:{model_type} {{ {fields} }}) RETURN t"
        res = session.run(query, model).single()
        return (Maybe.from_optional(res)
                .map(itemgetter("t"))
                .map(lambda x: dict(x))
                .value_or(None))

def delete_object(object_type, object_id):
    with driver.session() as session:
        query = (f"MATCH (t:{object_type})"
                 f"WHERE id(t) = {object_id}"
                 f" DELETE t")
        session.run(query)



def update_object(T, object_id, R=None):
    with driver.session() as session:
        model = asdict(T)
        if R:
            model.update(R)
        model_type = type(T).__name__
        fields = ", ".join([f"t.{k} = ${k}" for k in model.keys()])
        query = (f"MATCH (t:{model_type}) "
                 f"WHERE id(t) = {object_id}"
                 f" SET {fields} RETURN t")
        res = session.run(query, model).single()
        return (Maybe.from_optional(res)
                .map(itemgetter("t"))
                .map(lambda x: dict(x))
                .value_or(None))