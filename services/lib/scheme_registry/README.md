# Scheme Registry

## Development

1. Install dependencies

```bash
pip install -r requirements-dev.txt
```

2. Please make sure to check the code before pushing

```bash
black .
isort .
flake8 .
pytest
```

## How to generate schemes [optional]

1. Create pydantic classes in `schemes_generator`

2. Run command

```bash
python -m schemes_generator
```
