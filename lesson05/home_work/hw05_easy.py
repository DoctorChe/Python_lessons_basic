# Задача-1:
# Напишите скрипт, создающий директории dir_1 - dir_9 в папке,
# из которой запущен данный скрипт.
# И второй скрипт, удаляющий эти папки.

import os


def make_dir(dir_name):
    """
    Создаёт новую директорию с именем dir_name в текущей директории
    :param dir_name: имя новой директории
    :return: True - успешно, False - завершилось ошибкой
    """
    dir_path = os.path.join(os.getcwd(), dir_name)
    try:
        os.mkdir(dir_path)
        return True
    except FileExistsError:
        return False


def remove_dir(dir_name):
    """
    Удаляет директорию с именем dir_name в текущей директории
    :param dir_name: имя директории для удаления
    :return: True - успешно, False - завершилось ошибкой
    """
    dir_path = os.path.join(os.getcwd(), dir_name)
    try:
        os.rmdir(dir_path)
        return True
    except FileNotFoundError:
        return False


# Задача-2:
# Напишите скрипт, отображающий папки текущей директории.

def list_current_dir():
    files = os.listdir(path=os.getcwd())
    print("Список файлов в текущей директории:")
    for file in files:
        print(file)


# Задача-3:
# Напишите скрипт, создающий копию файла, из которого запущен данный скрипт.

def copy_current_script():
    """
    Создаёт копию файла, из которого запущен данный скрипт
    :return: True - успешно, False - завершилось ошибкой
    """

    import inspect, os
    print(inspect.getfile(inspect.currentframe()))

    import shutil
    try:
        file_path = os.getcwd()
        file_name = f"copy_{os.path.basename(__file__)}"
        file_full_name = os.path.join(file_path, file_name)
        shutil.copyfile(__file__, file_full_name)
        return True
    except Exception:
        return False


if __name__ == "__main__":

    for i in range(1, 10):
        dir_name = f"dir_{i}"
        if make_dir(f"dir_{i}"):
            print(f"Создана директория: {dir_name}")
        else:
            print(f"Такая директория уже существует: {dir_name}")

    for i in range(1, 10):
        dir_name = f"dir_{i}"
        if remove_dir(f"dir_{i}"):
            print(f"Удалена директория: {dir_name}")
        else:
            print(f"Такой директории не существует: {dir_name}")

    list_current_dir()

    if copy_current_script():
        print("Создана копия файла")
    else:
        print("Что-то пошло не так")
