import json
import pickle


def json_serialize(value: dict) -> bytes:
    return json.dumps(value).encode("utf-8")


def json_deserialize(data: bytes) -> dict:
    return json.loads(data.decode("utf-8"))


def pickle_serialize(value: dict) -> bytes:
    return pickle.dumps(value, pickle.HIGHEST_PROTOCOL)


def pickle_deserialize(data: bytes) -> dict:
    return pickle.loads(data)
