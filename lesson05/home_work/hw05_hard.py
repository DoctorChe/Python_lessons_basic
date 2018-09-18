# Задание-1:
# Доработайте реализацию программы из примера examples/5_with_args.py,
# добавив реализацию следующих команд (переданных в качестве аргументов):
#   cp <file_name> - создает копию указанного файла
#   rm <file_name> - удаляет указанный файл (запросить подтверждение операции)
#   cd <full_path or relative_path> - меняет текущую директорию на указанную
#   ls - отображение полного пути текущей директории
# путь считать абсолютным (full_path) -
# в Linux начинается с /, в Windows с имени диска,
# все остальные пути считать относительными.

# Важно! Все операции должны выполняться в той директории, в который вы находитесь.
# Исходной директорией считать ту, в которой был запущен скрипт.

# P.S. По возможности, сделайте кросс-платформенную реализацию.

# Данный скрипт можно запускать с параметрами:
# python hw05_hard.py param1 param2 param3
import os
import sys
import shutil

print('sys.argv = ', sys.argv)


def print_help():
    print("help - получение справки")
    print("mkdir <dir_name> - создание директории")
    print("cp <file_name> - создает копию указанного файла")
    print("rm <file_name> - удаляет указанный файл (запросить подтверждение операции)")
    print("cd <full_path or relative_path> - меняет текущую директорию на указанную")
    print("ls - отображение полного пути текущей директории")
    print("ping - тестовый ключ")


def make_dir():
    if not dir_name:
        print("Необходимо указать имя директории вторым параметром")
        return
    dir_path = os.path.join(os.getcwd(), dir_name)
    try:
        os.mkdir(dir_path)
        print('директория {} создана'.format(dir_name))
    except FileExistsError:
        print('директория {} уже существует'.format(dir_name))


def copy_file():
    """
    Создаёт копию файла, переданного параметром в скрипт
    """

    if not dir_name:
        print("Необходимо указать имя файла вторым параметром")
        return

    try:
        file_path = os.getcwd()
        file_name = f"copy_{os.path.basename(dir_name)}"
        file_full_name = os.path.join(file_path, file_name)
        shutil.copyfile(dir_name, file_full_name)
        print(f"Копия файла {dir_name} создана")
    except Exception:
        print("Что-то пошло не так")


def remove_file():
    """
    Удаляет файл, переданный параметром в скрипт
    """
    if not dir_name:
        print("Необходимо указать имя файла вторым параметром")
        return

    if input(f"Вы действительно хотите удалить файл: {dir_name}? (Y/N)").lower() == "y":
        try:
            file_full_name = os.path.join(os.getcwd(), dir_name)
            os.remove(file_full_name)
            print(f"Файл {dir_name} удалён")
        except FileNotFoundError:
            print(f"Файл {dir_name} не найден")


def change_dir():
    """
    Меняет текущую директорию на указанную, переданную параметром в скрипт
    """
    if not dir_name:
        print("Необходимо указать имя файла вторым параметром")
        return

    try:
        os.chdir(os.path.abspath(dir_name))
        print(f"Текущая директория сменена на {os.getcwd()}")
    except FileNotFoundError:
        print("Не верно задано имя директории")


def full_dir_path():
    """
    Выводит полный путь текущей директории
    """
    print(os.getcwd())


def ping():
    print("pong")


do = {
    "help": print_help,
    "mkdir": make_dir,
    "cp": copy_file,
    "rm": remove_file,
    "cd": change_dir,
    "ls": full_dir_path,
    "ping": ping
}

try:
    dir_name = sys.argv[2]
except IndexError:
    dir_name = None

try:
    key = sys.argv[1]
except IndexError:
    key = None


if key:
    if do.get(key):
        do[key]()
    else:
        print("Задан неверный ключ")
        print("Укажите ключ help для получения справки")
