import datetime as dt
import json
import pickle
import uuid


def json_default(obj):
    if isinstance(obj, dt.datetime):
        return {"_isoformat_datetime": obj.isoformat()}

    if isinstance(obj, dt.date):
        return {"_isoformat_date": obj.isoformat()}

    if isinstance(obj, uuid.UUID):
        return str(obj)

    raise TypeError(f"unsupported type {type(obj)=}")


def json_object_hook(obj):
    _isoformat = obj.get("_isoformat_date")
    if _isoformat is not None:
        return dt.date.fromisoformat(_isoformat)

    _isoformat = obj.get("_isoformat_datetime")
    if _isoformat is not None:
        return dt.datetime.fromisoformat(_isoformat)

    return obj


def json_serialize(value: dict) -> bytes:
    return json.dumps(value, default=json_default).encode("utf-8")


def json_deserialize(data: bytes) -> dict:
    return json.loads(data.decode("utf-8"), object_hook=json_object_hook)


def pickle_serialize(value: dict) -> bytes:
    return pickle.dumps(value, pickle.HIGHEST_PROTOCOL)


def pickle_deserialize(data: bytes) -> dict:
    return pickle.loads(data)
