import datetime as dt

import jsonschema


class Validator(jsonschema.Draft202012Validator):
    def is_type(self, instance, typ) -> bool:
        if isinstance(instance, dt.datetime) and typ == "string":
            return True
        return super().is_type(instance, typ)


@Validator.FORMAT_CHECKER.checks("date-time", ValueError)
def is_datetime(instance) -> bool:
    return isinstance(instance, dt.datetime)


def validate(schema, instance):
    jsonschema.validators.validate(instance, schema, cls=Validator)
