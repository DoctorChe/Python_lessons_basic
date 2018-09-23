# Задание-1:
# Реализуйте описаную ниже задачу, используя парадигмы ООП:
# В школе есть Классы(5А, 7Б и т.д.), в которых учатся Ученики.
# У каждого ученика есть два Родителя(мама и папа).
# Также в школе преподают Учителя. Один учитель может преподавать 
# в неограниченном кол-ве классов свой определенный предмет. 
# Т.е. Учитель Иванов может преподавать математику у 5А и 6Б,
# но больше математику не может преподавать никто другой.

# Выбранная и заполненная данными структура должна решать следующие задачи:
# 1. Получить полный список всех классов школы
# 2. Получить список всех учеников в указанном классе
#  (каждый ученик отображается в формате "Фамилия И.О.")
# 3. Получить список всех предметов указанного ученика 
#  (Ученик --> Класс --> Учителя --> Предметы)
# 4. Узнать ФИО родителей указанного ученика
# 5. Получить список всех Учителей, преподающих в указанном классе


class Person:
    """Класс для сущности человек"""

    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname

    def get_full_name(self):
        return f"{self.lastname} {self.firstname}"

    def display_information(self):
        print(self.__class__.__name__)
        # print('name:', self.firstname, self.lastname)
        print(f"name: {self.get_full_name()}")


class Student(Person):
    """Класс для сущности студент."""

    def __init__(self, firstname, father, mother, age, class_room):
        super().__init__(firstname, father.lastname)
        self.father = father
        self.mother = mother
        self.lastname = self.father.lastname
        self.age = age
        self.lessons = set()
        # self._class_room = {"class_num": int(self.class_room.splt()[0]),
        #                     "class_char": self.class_room.splt()[1]}
        self._class_room = {'class_num': int(class_room.split()[0]),
                            'class_char': class_room.split()[1]}

    @property
    def class_room(self):
        return "{} {}".format(self._class_room['class_num'], self._class_room['class_char'])

    # @property
    # def class_room(self):
    #     return f"{self._class_room['class_num']} {self._class_room['class_char']}"

    def get_full_name(self):
        return f"{self.lastname} {self.firstname[0].upper()}. {self.father.firstname[0].upper()}."

    def next_class(self):
        self._class_room["class_num"] += 1

    def participate(self, lesson):
        """присоединится к лекции."""
        lesson.add_student(self)

    def display_information(self, lessons):
        """Печатает информацию о студенте"""
        super().display_information()
        print('age:', self.age)
        print("lessons:")
        for l in lessons.lessons_by_student(self):
            print(l)


class Teacher(Person):
    """Класс для сущности преподователь"""

    def __init__(self, firstname, lastname):
        super().__init__(firstname, lastname)
        # self.teach_classes = list(map(self.convert_class, teach_classes))

    def convert_class(self, class_room):
        return {"class_num": int(class_room.splt()[0]),
                "class_char": class_room.splt()[1]}

    def participate(self, lesson):
        """Взять курс для обучения."""
        lesson.teacher = self

    def display_information(self, lessons):
        super().display_information()
        print("lessons:")
        for l in lessons.lessons_by_teacher(self):
            print(l)


class School:
    """Описывает понятие школа"""

    def __init__(self):
        self.classes = []


class ClassRoom:

    def __init__(self, location, seats):
        self.location = location
        self.seats_num = seats


class Lesson:
    """Описывает понятие Урок."""

    def __init__(self):
        self.name = None
        self.hours = 0
        self.classroom = None
        self._students = []
        self._teacher = None

    def add_student(self, student):
        if len(self._students) < self.classroom.seats_num:
            self._students.append(student)
        else:
            raise ValueError("no seats")

    def has_student(self, student):
        """Проверяет что данный студент записан на курс"""
        return student in self._students

    @property
    def teacher(self):
        return self._teacher

    @teacher.setter
    def teacher(self, teacher):
        if self._teacher is not None:
            raise ValueError("already has teacher")
        self._teacher = teacher

    def __str__(self):
        return f'name:{self.name}; hours:{self.hours}'


class Scheduler:
    def __init__(self):
        self._lessons = {}

    def add_lesson(self, name, hours, classroom):
        python_lesson = Lesson()
        python_lesson.name = name
        python_lesson.hours = hours
        python_lesson.classroom = classroom
        self._lessons[name] = python_lesson

    def get_lesson(self, name):
        try:
            return self._lessons[name]
        except KeyError:
            raise ValueError(f"there is no lesson with name {name}")

    def lessons_by_teacher(self, teacher):
        """Возвращает список курсов, которые ведет указанный преподователь."""
        result = []
        for l in self._lessons.values():
            if l.teacher is teacher:
                result.append(l)
        return result

    def lessons_by_student(self, student):
        """Возвращает список курсов, на которые записан студент."""
        result = []
        for l in self._lessons.values():
            if l.has_student(student):
                result.append(l)
        return result


persons = [
    Student("Ivan", Person("Sergei", "Ivanov"), Person("Maria", "Ivanova"), 16, "5 А"),
    Student("Petr", Person("Ivan", "Sergeev"), Person("Klavdia", "Sergeeva"), 17, "8 Г"),
    Teacher("Fedor", "Petrov"),
    # Teacher("Boris", "Sergeev"),
]

scheduler = Scheduler()

scheduler.add_lesson("python", 16, ClassRoom("web", 2))

print("Persons:")

for person in persons:
    person.participate(scheduler.get_lesson("python"))

for person in persons:
    person.display_information(scheduler)

# print()
# for person in persons:
#     if person.__class__ == Student:
#         print(f"Parents of {person.get_full_name()}")
#         print("Father")
#         person.father.display_information()
#         print("Mother")
#         person.mother.display_information()

print()
for person in persons:
    if person.__class__ == Student:
        print(f"Lessons of {person.get_full_name()}")
        for l in person.lessons:
            print(l)
