# Задание-1: Решите задачу (дублированную ниже):

# Дана ведомость расчета заработной платы (файл "data/workers").
# Рассчитайте зарплату всех работников, зная что они получат полный оклад,
# если отработают норму часов. Если же они отработали меньше нормы,
# то их ЗП уменьшается пропорционально, а за заждый час переработки они получают
# удвоенную ЗП, пропорциональную норме.
# Кол-во часов, которые были отработаны, указаны в файле "data/hours_of"

# С использованием классов.
# Реализуйте классы сотрудников так, чтобы на вход функции-конструктора
# каждый работник получал строку из файла

import os


class Worker:
    def __init__(self, line):
        self.name = line.split()[0]
        self.lastname = line.split()[1]
        self.salary = int(line.split()[2])
        self.job = line.split()[3]
        self.standard_hours = int(line.split()[4])
        self.full_name = f"{self.name} {self.lastname}"

    def wage_count(self, hours):
        overtime = hours - self.standard_hours
        return int(self.salary * (1 + 2 * overtime / self.standard_hours)
                   if overtime > 0 else self.salary * (1 + overtime / self.standard_hours))


workers = []
path = os.path.join('data', 'workers')
with open(path, "r", encoding='UTF-8') as f:
    f.readline()  # Удаляем заголовок таблицы
    for line in f.readlines():
        workers.append(Worker(line))

path = os.path.join('data', 'hours_of')
with open(path, "r", encoding='UTF-8') as f:
    f.readline()  # Удаляем заголовок таблицы
    hours_of = f.readlines()

hours_of_worker = {}
for hours in hours_of:
    hours_data = hours.split()
    worker = f"{hours_data[0]} {hours_data[1]}"  # Работник (Имя Фамилия)
    hours_of_worker[worker] = hours_data[2]

wage_dict = {}  # Словарь для хранения зарплат, начисленных с учётом переработок

for worker in workers:
    wage_dict[worker.full_name] = worker.wage_count(int(hours_of_worker[worker.full_name]))

# Выводим на печать таблицу зарплат, начисленных с учётом переработок
align = max(map(len, wage_dict.keys()))
print(f"Работник         Зарплата")
for k, v in wage_dict.items():
    print(f"{k} {v:>{align - len(k) + 6}}")
