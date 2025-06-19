import logging

from sqlmodel import Session, select

from src.models import Student
from src.utils import engine


class StudentService:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def get_all(self):
        self.logger.info("fetch all students!")
        with Session(engine) as session:
            students = session.exec(select(Student)).all()
            return students
