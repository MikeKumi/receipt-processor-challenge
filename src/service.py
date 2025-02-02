from jsonschema import validate, ValidationError
from src.schemas.receipt import receipt_schema


def process_receipt_json(json_dict):
    try:
        validate(json_dict, receipt_schema)
    except ValidationError:
        pass
