import functools
import json
import os
import pathlib
import typing as ty

from scheme_registry.validate import validate


class SchemeRegistry:
    def __init__(self, schemes_path: ty.Union[os.PathLike, str, None] = None):
        default_path = pathlib.Path(__file__).parent / "schemes"
        self.schemes_path = str(schemes_path or default_path)

    def validate_event(self, data: dict, name: str, version: int = 1, raise_error: bool = False) -> bool:
        try:
            scheme = self._load_scheme(name, version)
            validate(instance=data, schema=scheme)
        except Exception:
            if raise_error:
                raise
            return False
        return True

    @functools.lru_cache(maxsize=None)
    def _load_scheme(self, name: str, version: int) -> dict:
        path_parts = name.split(".")
        full_path = os.path.join(self.schemes_path, *path_parts, f"{version}.json")
        with open(full_path, "r") as fd:
            return json.load(fd)
