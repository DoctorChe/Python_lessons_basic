# Задание-1:
# Написать программу, выполняющую операции (сложение и вычитание) с простыми дробями.
# Дроби вводятся и выводятся в формате:
# n x/y ,где n - целая часть, x - числитель, у - знаменатель.
# Дроби могут быть отрицательные и не иметь целой части, или иметь только целую часть.
# Примеры:
# Ввод: 5/6 + 4/7 (всё выражение вводится целиком в виде строки)
# Вывод: 1 17/42  (результат обязательно упростить и выделить целую часть)
# Ввод: -2/3 - -2
# Вывод: 1 1/3


def gcd(a, b):
    """
    НОД - наибольший общий делитель
    :param a:
    :param b:
    :return:
    """
    while a != 0 and b != 0:
        if a > b:
            a %= b
        else:
            b %= a

    return a + b


def set_fraction(frac):
    """
    Преобразование строки во внутреннее представление дроби
    :param frac: строка (дробь)
    :return: словарь (внутреннее представление дроби)
    """
    if len(frac) > 0:
        minus = frac[0] == "-"
        if minus:
            frac = frac[1:]
        if frac.find(" ") != -1:
            integer, _, fractional = frac.partition(" ")
        elif frac.find("/") != -1:
            integer = ""
            fractional = frac
        else:
            integer = frac
            fractional = ""
        if fractional:
            numerator, _, denominator = fractional.partition("/")
        else:
            numerator = ""
            denominator = ""
        return {"minus": minus, "integer": integer, "numerator": numerator, "denominator": denominator}
    else:
        return {"minus": True, "integer": "0", "numerator": "0", "denominator": "1"}


def get_fraction(frac):
    """
    Преобразование внутреннего предствления дроби в строку
    :param frac: словарь (внутреннее представление дроби)
    :return: строка (дробь)
    """
    minus = "-" if frac["minus"] else ""
    integer = frac["integer"] if frac["integer"] != "0" else ""
    numerator = frac["numerator"] if frac["numerator"] != "0" else ""
    denominator = frac["denominator"] if frac["denominator"] != "1" else "1"
    if frac["integer"] != "0" and frac["numerator"] != "0":
        return f"{minus}{integer} {numerator}/{denominator}"
    elif frac["integer"] != "0" and frac["numerator"] == "0":
        return f"{minus}{integer}"
    elif frac["integer"] == "0" and frac["numerator"] != "0":
        return f"{minus}{numerator}/{denominator}"


def do_operation(expression):

    if expression.find("+") != -1:
        a, operation, b = expression.partition(" + ")
    else:
        a, operation, b = expression.partition(" - ")

    a = set_fraction(a)
    b = set_fraction(b)

    m1 = -1 if a.get("minus") else 1
    m2 = -1 if b.get("minus") else 1
    i1 = int(a.get("integer")) if a.get("integer") != "" else 0
    i2 = int(b.get("integer")) if b.get("integer") != "" else 0
    n1 = int(a.get("numerator")) if a.get("numerator") != "" else 0
    n2 = int(b.get("numerator")) if b.get("numerator") != "" else 0
    d1 = int(a.get("denominator")) if a.get("denominator") != "" else 1
    d2 = int(b.get("denominator")) if b.get("denominator") != "" else 1

    if operation == " + ":
        n3 = m1 * (i1 * d1 + n1) * d2 + m2 * (i2 * d2 + n2) * d1
    else:
        n3 = m1 * (i1 * d1 + n1) * d2 - m2 * (i2 * d2 + n2) * d1

    d3 = d1 * d2
    minus = n3 < 0
    m3 = -1 if minus else 1
    n3 *= m3
    if abs(n3 / d3) > 1:
        i3 = int(n3 // d3)
        n3 = int(n3 % d3)
    else:
        i3 = 0
    if n3 and d3:
        gcd_c = gcd(n3, d3)
    else:
        gcd_c = 1
    n3 = int(n3 / gcd_c)
    d3 = int(d3 / gcd_c)

    c = {"minus": minus, "integer": str(i3), "numerator": str(n3), "denominator": str(d3)}
    return c


expression = "5/6 + 4/7"
print(f"Ввод: {expression}")
print(f"Вывод: {get_fraction(do_operation(expression))}")

expression = "-2/3 - -2"
print(f"Ввод: {expression}")
print(f"Вывод: {get_fraction(do_operation(expression))}")


# Задание-2:
# Дана ведомость расчета заработной платы (файл "data/workers").
# Рассчитайте зарплату всех работников, зная что они получат полный оклад,
# если отработают норму часов. Если же они отработали меньше нормы,
# то их ЗП уменьшается пропорционально, а за заждый час переработки
# они получают удвоенную ЗП, пропорциональную норме.
# Кол-во часов, которые были отработаны, указаны в файле "data/hours_of"

import os

path = os.path.join('data', 'workers')
with open(path, "r", encoding='UTF-8') as f:
    workers = f.readlines()

path = os.path.join('data', 'hours_of')
with open(path, "r", encoding='UTF-8') as f:
    hours_of = f.readlines()

workers_dict = {}  # Словарь для хранения данных о работниках
workers.pop(0)  # Удаляем заголовок таблицы

for worker in workers:
    worker_data = worker.split()
    workers_dict[f"{worker_data[0]} {worker_data[1]}"] = [worker_data[2], worker_data[4]]

wage_dict = {}  # Словарь для хранения зарплат, начисленных с учётом переработок
hours_of.pop(0)  # Удаляем заголовок таблицы

for hours in hours_of:
    hours_data = hours.split()
    worker = f"{hours_data[0]} {hours_data[1]}"  # Работник (Имя Фамилия)
    salary = int(workers_dict[worker][0])  # Оклад
    standard_hours = int(workers_dict[worker][1])  # Норма_часов
    overtime = int(hours_data[2]) - int(workers_dict[worker][1])  # Переработка

    # Вычисляем зарплату с учётом переработок
    wage = int(salary * (1 + 2 * overtime / standard_hours) if overtime > 0 else salary * (1 + overtime / standard_hours))
    wage_dict[worker] = wage  # Добавляем данные в словарь

# Выводим на печать таблицу зарплат, начисленных с учётом переработок
align = max(map(len, wage_dict.keys()))
print(f"Работник         Зарплата")
for k, v in wage_dict.items():
    print(f"{k} {v:>{align - len(k) + 6}}")


# Задание-3:
# Дан файл ("data/fruits") со списком фруктов.
# Записать в новые файлы все фрукты, начинающиеся с определенной буквы.
# Т.е. в одном файле будут все фрукты на букву “А”, во втором на “Б” и т.д.
# Файлы назвать соответственно.
# Пример имен файлов: fruits_А, fruits_Б, fruits_В ….
# Важно! Обратите внимание, что нет фруктов, начинающихся с некоторых букв.
# Напишите универсальный код, который будет работать с любым списком фруктов
# и распределять по файлам в зависимости от первых букв, имеющихся в списке фруктов.
# Подсказка:
# Чтобы получить список больших букв русского алфавита:
# print(list(map(chr, range(ord('А'), ord('Я')+1))))

import os

path = os.path.join('data', 'fruits.txt')
with open(path, "r", encoding='UTF-8') as f:
    fruits = f.readlines()
try:
    for fruit in fruits:
        if fruit != "\n":
            path = os.path.join('data', f'fruits_{fruit[0]}.txt')
            with open(path, "a", encoding='UTF-8') as f:
                f.write(fruit)
except FileExistsError:
    with open(path, "x", encoding='UTF-8') as f:
        f.write(fruit)
