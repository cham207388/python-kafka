import json
from pydantic import EmailStr, field_validator, ConfigDict
from typing import Optional
from sqlmodel import Field, SQLModel

class Student(SQLModel, table=True):
    __tablename__ = "students"
    
    id: Optional[str] = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True, nullable=False)
    first_name: str = Field(max_length=50, nullable=False)
    last_name: str = Field(max_length=50, nullable=False)
    
    @field_validator("first_name", "last_name")
    def validate_name(cls, value):
        if not value.strip():
            raise ValueError("Name cannot be empty")
        return value
     
def to_student(value) -> Student:
    student_dict = json.loads(value.decode())
    student_obj = Student.model_validate(student_dict)
    return student_obj