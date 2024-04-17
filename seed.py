import random
import sqlalchemy
from datetime import datetime

from faker import Faker
from connect import session
from models import Group, Students, Teachers, Subjects, Marks, Base

Faker.seed(1)
fake = Faker(locale='uk-UA')


def clear_tables(session):
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())
        sequence_name = f"{table.name}_id_seq"
        stmt = sqlalchemy.text(f"ALTER SEQUENCE {sequence_name} RESTART WITH 1")
        session.execute(stmt)
    session.commit()


clear_tables(session)

# Groups
for _ in range(3):
    group = Group(name=fake.random_number(digits=3, fix_len=True))
    session.add(group)

# Teachers
for _ in range(5):
    teacher = Teachers(name=fake.first_name(), lastname=fake.last_name())
    session.add(teacher)

# Subjects
subjects = [
    'Математика',
    'Фізика',
    'Інформатика',
    'Інженарія',
    'Психологія',
    'Соціологія',
    'Полоітологія',
    'Філософія'
]
t_id_list = []
for t in session.query(Teachers).all():
    t_id_list.append(t.id)
    
for i in subjects:
    subject = Subjects(name=i, teacher_id=random.choice(t_id_list))
    session.add(subject)

# Students
for _ in range(50):
    student = Students(name=fake.first_name(),
                        lastname=fake.last_name(),
                        group_id=random.choice([i.id for i in session.query(Group).all()]))
    session.add(student)

# Marks
get_students = session.query(Students).all()
get_subjects = session.query(Subjects).all()

for student in get_students:
    for _ in range(20):
        random_subject = random.choice(get_subjects)
        mark = Marks(student_id=student.id,
                    subject_id=random_subject.id,
                    mark=random.randint(1, 5),
                    date=fake.date_between_dates(date_start=datetime(2023,1,1),
                                                date_end=datetime(2023,6,1)))
        session.add(mark)

session.commit()
session.close()
    





