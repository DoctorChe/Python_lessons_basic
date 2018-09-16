# Задача-1:
# Напишите скрипт, создающий директории dir_1 - dir_9 в папке,
# из которой запущен данный скрипт.
# И второй скрипт, удаляющий эти папки.

import os


def make_dirs():
    for i in range(1, 10):
        dir_path = os.path.join(os.getcwd(), f'dir_{i}')
        try:
            # Создаем новую директорию
            os.mkdir(dir_path)
            print(f'Создана директория: {dir_path}')
        except FileExistsError:
            print(f'Такая директория уже существует: {dir_path}')


def remove_dirs():
    for i in range(1, 10):
        dir_path = os.path.join(os.getcwd(), f'dir_{i}')
        try:
            # Удаляем существующую пустую директорию
            os.rmdir(dir_path)
            print(f'Удалена директория: {dir_path}')
        except FileNotFoundError:
            print(f'Такой директории не существует: {dir_path}')


make_dirs()
remove_dirs()


# Задача-2:
# Напишите скрипт, отображающий папки текущей директории.

def list_current_dir():
    files = os.listdir(path=os.getcwd())
    print(f'Список файлов в текущей директории:')
    for file in files:
        print(file)


list_current_dir()


# Задача-3:
# Напишите скрипт, создающий копию файла, из которого запущен данный скрипт.

def copy_current_script():
    global file_path
    import shutil
    try:
        file_path = os.path.join(os.getcwd(), f'copy_{os.path.basename(__file__)}')
        shutil.copyfile(__file__, file_path)
        print(f'Создана копия файла: {file_path}')
    except Exception:
        print('Что-то пошло не так')


copy_current_script()
