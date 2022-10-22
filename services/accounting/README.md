# Backend

## Development

1. Install dependencies

```bash
pip install -r requirements-dev.txt
```

2. Make `.env` file (you can make it based on `.env.template`)

```bash
cp .env.template .env
```

3. Please make sure to check the code before pushing

```bash
black .
isort .
flake8 .
pytest
```

## How to start

1. Configure DB in `.env` file

2. Apply migrations

```bash
python manage.py migrate
```

3. Prepare initial data

```bash
python manage.py createsuperuser
```

## TODO

Problem with django-kafka-consumer admin page: `from_db_value() missing 1 required positional argument: 'context'`

Solution: https://github.com/stephenmcd/mezzanine/issues/1971#issuecomment-724380235

`.../site-packages/kafka_consumer/fields.py:37`

---
