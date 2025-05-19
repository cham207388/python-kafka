from jsonschema import validate, Draft202012Validator
from typing import Dict
from src.config import STUDENT_JSON_SCHEMA

class StudentSchemaValidator:
    def __init__(self, schema: Dict = STUDENT_JSON_SCHEMA):
        self.validator = Draft202012Validator(schema)

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