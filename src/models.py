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
     
def deserialize(value) -> Student:
    print(value)
    print(type(value))
    student_obj = Student.model_validate(value)
    return student_obj

def to_student(request: dict) -> Student:
    return Student(
        email=request.get("email"),
        first_name=request.get("first_name"),
        last_name=request.get("last_name")
    )

def student_dict(student, ctx):
    if student is None:
        print("🚨 Attempted to serialize a None value")
        return {}
    return student.dict()