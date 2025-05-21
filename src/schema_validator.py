from jsonschema import validate, Draft202012Validator
from typing import Dict
STUDENT_JSON_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://com.abc.learning/student.schema.json",
    "title": "Student",
    "type": "object",
    "properties": {
        "id": {
            "type": ["string", "null"]
        },
        "email": {
            "type": "string",
            "format": "email"
        },
        "first_name": {
            "type": "string"
        },
        "last_name": {
            "type": "string"
        }
    },
    "required": ["email", "first_name", "last_name"],
    "additionalProperties": False
}

class StudentSchemaValidator:
    def __init__(self, schema: Dict = STUDENT_JSON_SCHEMA):
        self.schema = schema
        self.validator = Draft202012Validator(self.schema)

    def is_valid(self, student_data: Dict) -> bool:
        """Returns True if student data is valid, False otherwise."""
        return self.validator.is_valid(student_data)

    def validate_or_raise(self, student_data: Dict) -> None:
        """
        Validates the student data against the schema.
        Raises ValidationError if invalid.
        """
        validate(instance=student_data, schema=STUDENT_JSON_SCHEMA)

    def get_errors(self, student_data: Dict):
        """Returns a list of validation error messages."""
        return [error.message for error in self.validator.iter_errors(student_data)]