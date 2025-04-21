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
      
class StudentRequest(SQLModel):
    id: Optional[str] = None
    email: EmailStr  # ✅ Enforces email validation
    first_name: str = Field(..., min_length=3, max_length=15)
    last_name: str = Field(..., min_length=3, max_length=15)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "username@email.com",
                "first_name": "First Name",
                "last_name": "Last Name"
            }
        }
    )

    @field_validator("first_name", "last_name")
    def validate_name(cls, value):
        if not value.strip():
            raise ValueError("Name cannot be empty")
        return value
      
def to_user(request: dict) -> Student:
    return Student(
        email=request.get("email"),
        first_name=request.get("first_name"),
        last_name=request.get("last_name")
    )