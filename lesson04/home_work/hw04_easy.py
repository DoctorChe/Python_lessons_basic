# Все задачи текущего блока решите с помощью генераторов списков!

# Задание-1:
# Дан список, заполненный произвольными целыми числами. 
# Получить новый список, элементы которого будут
# квадратами элементов исходного списка
# [1, 2, 4, 0] --> [1, 4, 16, 0]

try:
    lst = list(map(int, input("Введите список целых чисел, разделённых запятыми: ").replace(",", " ").split()))
    lst_sqr = [x * x for x in lst]
    print(f"{lst} --> {lst_sqr}")
except ValueError:
    print("Введены некорректные данные")


# Задание-2:
# Даны два списка фруктов.
# Получить список фруктов, присутствующих в обоих исходных списках.

# fruits1 = ["яблоко", "апельсин", "банан"]
# fruits2 = ["малина", "банан", "апельсин"]

fruits1 = input("Введите первый список фруктов, разделённых запятыми: ").replace(",", " ").split()
fruits2 = input("Введите второй список фруктов, разделённых запятыми: ").replace(",", " ").split()

common_fruits = [x for x in fruits1 if x in fruits2]

print(f"Список фруктов, присутствующих в обоих исходных списках: {common_fruits}")


# Задание-3:
# Дан список, заполненный произвольными числами.
# Получить список из элементов исходного, удовлетворяющих следующим условиям:
# + Элемент кратен 3
# + Элемент положительный
# + Элемент не кратен 4

try:
    # lst = [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    lst = list(map(int, input("Введите список чисел, разделённых запятыми: ").replace(",", " ").split()))
    lst_new = [x for x in lst if x % 3 == 0 and x > 0 and x % 4 != 0]
    print(f"{lst} --> {lst_new}")
except ValueError:
    print("Введены некорректные данные")