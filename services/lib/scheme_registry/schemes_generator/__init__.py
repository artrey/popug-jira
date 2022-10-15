import importlib
import json
import os
import pathlib

from pydantic import BaseModel


def generate_json_schemes(root_output_path: str):
    generator_package_path = pathlib.Path(__file__).parent
    modules = sorted([x.stem for x in generator_package_path.iterdir() if not x.stem.startswith("__")])
    print(f"Found {len(modules)} domain(s): {modules}")

    for module in modules:
        module = f"{generator_package_path.stem}.{module}"
        print(f"Generate schemes from {module}")

        module = importlib.import_module(module)
        for entity in vars(module).values():
            try:
                if not issubclass(entity, (BaseModel,)) or entity is BaseModel:
                    continue
            except:  # noqa E722
                continue

            entity_name, version = entity.__name__.rsplit("V", maxsplit=1)
            entity_module_path = entity.__module__.split(".")

            scheme_folder = os.path.join(root_output_path, *entity_module_path[1:], entity_name)
            os.makedirs(scheme_folder, exist_ok=True)

            scheme_path = os.path.join(scheme_folder, f"{version}.json")
            with open(scheme_path, "w", encoding="utf-8") as fd:
                json.dump(entity.schema(), fd, indent=2, ensure_ascii=False)
                print(f"* Generated scheme: {entity.__name__}")
