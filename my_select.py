import sys
from connect import session
from models import Students, Subjects, Teachers, Marks, Group
from sqlalchemy import func, desc
from prettytable import PrettyTable


def table(field_names, data):   
    table = PrettyTable()
    table.field_names = field_names
    for i in data: 
        table.add_row(i)
    return table


def select_1():
    print("Завдання: Знайти 5 студентів із найбільшим середнім балом з усіх предметів")
    field_names = ['namae', 'lastname', 'averege mark']
    data = session.query(Students.name, Students.lastname,  func.round(func.avg(Marks.mark), 2).label('avg_grade'))\
        .select_from(Marks).join(Students).group_by(Students.id).order_by(desc('avg_grade')).limit(5).all()
    return table(field_names, data)


def select_2():
    print("Завдання: Знайти студента із найвищим середнім балом з певного предмета.")
    subject = input('Введіть назву предмета: ')
    field_names = ['name', 'lastname', 'subject', 'averege mark']
    data = session.query(Students.name,
                        Students.lastname,
                        Subjects.name,
                        func.round(func.avg(Marks.mark), 2).label('avg_grade'))\
                        .select_from(Students).join(Marks, Students.id == Marks.student_id)\
                        .join(Subjects, Subjects.id == Marks.subject_id)\
                        .filter(Subjects.name==subject).group_by(Students.name, Students.lastname, Subjects.name)\
                        .order_by(desc('avg_grade')).limit(1).all()
    return table(field_names, data)

def select_3():
    print("Завдання: Знайти середній бал у групах з певного предмета.")
    subject = input('Введіть назву предмета: ')
    field_names = ['name', 'subject', 'averege mark']
    data = session.query(Group.name,
                        Subjects.name,
                        func.round(func.avg(Marks.mark), 2).label('avg_grade'))\
                        .select_from(Group).join(Students, Students.group_id == Group.id)\
                        .join(Marks, Students.id == Marks.student_id)\
                        .join(Subjects, Subjects.id == Marks.subject_id)\
                        .filter(Subjects.name==subject).group_by(Group.name, Subjects.name)\
                        .order_by(desc('avg_grade')).all()
    return table(field_names, data)

def select_4():
    print("Завдання: Знайти середній бал на потоці (по всій таблиці оцінок).")
    field_names = ['name', 'averege mark']
    data = session.query(Group.name,
                        func.round(func.avg(Marks.mark), 2).label('avg_grade'))\
                        .select_from(Group).join(Students, Students.group_id == Group.id)\
                        .join(Marks, Students.id == Marks.student_id)\
                        .group_by(Group.name)\
                        .order_by(desc('avg_grade')).all()
    return table(field_names, data)

def select_5():
    print("Завдання: Знайти які курси читає певний викладач.")
    name, lastname = input('Введіть ім\'я та прізвище викладача: ').split()
    field_names = ['name', 'lastname', 'subject']
    data = session.query(Teachers.name, Teachers.lastname, Subjects.name)\
                        .select_from(Subjects).join(Teachers, Subjects.teacher_id == Teachers.id)\
                        .filter(Teachers.name==name, Teachers.lastname==lastname)\
                        .order_by(Teachers.lastname).all()
    return table(field_names, data)

def select_6():
    print("Завдання: Знайти список студентів у певній групі.")
    group_num = input('Введіть номер групи: ')
    field_names = ['group', 'name', 'lastname']
    data = session.query(Group.name, Students.name, Students.lastname)\
                        .select_from(Group).join(Students, Students.group_id == Group.id)\
                        .filter(Group.name==group_num)\
                        .order_by(Students.lastname).all()
    return table(field_names, data)

def select_7():
    print("Завдання: Знайти оцінки студентів у окремій групі з певного предмета.")
    group_num = input('Введіть номер групи: ')
    subject = input('Введіть назву предмета: ')
    field_names = ['group', 'name', 'lastname', 'subject', 'mark', 'date']
    data = session.query(Group.name, Students.name, Students.lastname, Subjects.name, Marks.mark, Marks.date)\
                        .select_from(Marks).join(Students, Students.id == Marks.student_id)\
                        .join(Subjects, Subjects.id == Marks.subject_id)\
                        .join(Group, Students.group_id == Group.id)\
                        .filter(Group.name==group_num, Subjects.name==subject)\
                        .order_by(Students.lastname).all()
    return table(field_names, data)

def select_8():
    print("Завдання: Знайти середній бал, який ставить певний викладач зі своїх предметів.")
    name, lastname = input('Введіть ім\'я та прізвище викладача: ').split()
    field_names = ['name', 'lastname', 'subject', 'averege mark']
    data = session.query(Teachers.name,
                        Teachers.lastname,
                        Subjects.name,
                        func.round(func.avg(Marks.mark), 2).label('avg_grade'))\
                        .select_from(Marks).join(Subjects, Subjects.id == Marks.subject_id)\
                        .join(Teachers, Subjects.teacher_id == Teachers.id)\
                        .filter(Teachers.name==name, Teachers.lastname==lastname)\
                        .group_by(Teachers.name, Teachers.lastname, Subjects.name).order_by(Subjects.name).all()
    return table(field_names, data)

def select_9():
    print("Завдання: Знайти список курсів, які відвідує студент.")
    name, lastname = input('Введіть ім\'я та прізвище студента: ').split()
    field_names = ['name', 'lastname', 'subject']
    data = session.query(Students.name,
                        Students.lastname,
                        Subjects.name)\
                        .select_from(Students).join(Marks, Students.id == Marks.student_id)\
                        .join(Subjects, Marks.subject_id == Subjects.id)\
                        .filter(Students.name==name, Students.lastname==lastname)\
                        .group_by(Students.name, Students.lastname, Subjects.name).order_by(Subjects.name).all()
    return table(field_names, data)

def select_10():
    print("Завдання: Список курсів, які певному студенту читає певний викладач.")
    s_name, s_lastname = input('Введіть ім\'я та прізвище студента: ').split()
    t_name, t_lastname = input('Введіть ім\'я та прізвище викладача: ').split()
    field_names = [ 'studnet name',
                   'student lastname',
                   'teacher name',
                   'teacher lastname',
                   'subject']
    
    data = session.query(Students.name,
                        Students.lastname,
                        Teachers.name,
                        Teachers.lastname,
                        Subjects.name)\
                        .select_from(Students).join(Marks, Students.id == Marks.student_id)\
                        .join(Subjects, Marks.subject_id == Subjects.id)\
                        .join(Teachers, Subjects.teacher_id== Teachers.id)\
                        .filter(Students.name==s_name,
                                Students.lastname==s_lastname,
                                Teachers.name==t_name,
                                Teachers.lastname==t_lastname)\
                        .group_by(Students.name,
                                    Students.lastname,
                                    Teachers.name,
                                    Teachers.lastname,
                                    Subjects.name).all()
    return table(field_names, data)

def exit():
    print('Good bye')
    sys.exit()

selects = {
    '0': exit,
    '1': select_1,
    '2': select_2,
    '3': select_3,
    '4': select_4,
    '5': select_5,
    '6': select_6,
    '7': select_7,
    '8': select_8,
    '9': select_9,
    '10': select_10
}
help = {
    '0': 'Вихід',
    '1': 'Знайти 5 студентів із найбільшим середнім балом з усіх предметів',
    '2': 'Знайти студента із найвищим середнім балом з певного предмета.',
    '3': 'Знайти середній бал у групах з певного предмета.',
    '4': 'Знайти середній бал на потоці (по всій таблиці оцінок).',
    '5': 'Знайти які курси читає певний викладач.',
    '6': 'Знайти список студентів у певній групі.',
    '7': 'Знайти оцінки студентів у окремій групі з певного предмета.',
    '8': 'Знайти середній бал, який ставить певний викладач зі своїх предметів.',
    '9': 'Знайти список курсів, які відвідує студент.',
    '10': 'Список курсів, які певному студенту читає певний викладач.'
}

help_str = ''
for key, value in help.items():
    help_str += '{} -> {}\n'.format(key, value)

def get_handler(user_input):
    return selects.get(user_input)

def main():
    while True:
        user_input = input('>> ')
        handler = get_handler(user_input)
        try:
            result = handler()
            print(result)
        except TypeError:
            print(f'Не знайома команда! Виберіть зі списку команд: \n')
            print(help_str)


if __name__ == '__main__':
    main()

