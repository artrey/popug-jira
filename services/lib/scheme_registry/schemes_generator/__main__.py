from schemes_generator import generate_json_schemes

if __name__ == "__main__":
    import pathlib

    base_dir = pathlib.Path(__file__).parent.parent
    generate_json_schemes(str(base_dir / "scheme_registry" / "schemes"))
