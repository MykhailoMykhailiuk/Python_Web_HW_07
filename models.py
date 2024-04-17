from sqlalchemy import String, ForeignKey, DATE, Integer
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
    )

from connect import Base, engine


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(5))
    student: Mapped['Students'] = relationship(back_populates='group')

    def __repr__(self) -> str:
        return f"{self.id}, {self.name}"


class Students(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    lastname: Mapped[str] = mapped_column(String(25))
    group_id: Mapped[int] = mapped_column(ForeignKey('groups.id'))
    group: Mapped['Group'] = relationship(back_populates='student')

    def __repr__(self) -> str:
        return f"{self.id}, {self.name}, {self.lastname}"
    

class Teachers(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    lastname: Mapped[str] = mapped_column(String(25))
    subject: Mapped['Subjects'] = relationship(back_populates='teacher')

    def __repr__(self) -> str:
        return f"{self.id}, {self.name}, {self.lastname}"
    

class Subjects(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    teacher_id: Mapped[int] = mapped_column(ForeignKey('teachers.id'))
    teacher: Mapped['Teachers'] = relationship(back_populates='subject')

    def __repr__(self) -> str:
        return f"{self.id}, {self.name}"
    

class Marks(Base):
    __tablename__ = "marks"

    id: Mapped[int] = mapped_column(primary_key=True)
    mark: Mapped[int] = mapped_column()
    date: Mapped[str] = mapped_column(DATE)
    student_id: Mapped[int] = mapped_column(ForeignKey('students.id'))
    subject_id: Mapped[int] = mapped_column(ForeignKey('subjects.id'))

    def __repr__(self) -> str:
        return f"{self.id}, {self.mark}"
