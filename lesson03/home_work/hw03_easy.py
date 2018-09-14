# Задание-1:
# Напишите функцию, округляющую полученное произвольное десятичное число
# до кол-ва знаков (кол-во знаков передается вторым аргументом).
# Округление должно происходить по математическим правилам (0.6 --> 1, 0.4 --> 0).
# Для решения задачи не используйте встроенные функции и функции из модуля math.


def my_round(number, ndigits):
    delimiter = str(number).find(".")
    number_str_tmp = ""
    number_str = str(number)[:delimiter + ndigits + 1]
    digit_last = int(str(number)[delimiter + ndigits + 1])

    if digit_last >= 5:
        count = len(number_str)
        extra = True
        while count > 0:
            if number_str[count - 1] != ".":
                digit_tmp = str(int(number_str[count - 1]) + extra)
                extra = True if len(digit_tmp) > 1 else False
                number_str_tmp = digit_tmp[-1] + number_str_tmp
            else:
                number_str_tmp = "." + number_str_tmp
            count -= 1

    return float(number_str_tmp)


print(my_round(2.1234567, 5))
print(my_round(2.1999967, 5))
print(my_round(2.9999967, 5))


# Задание-2:
# Дан шестизначный номер билета. Определить, является ли билет счастливым.
# Решение реализовать в виде функции.
# Билет считается счастливым, если сумма его первых и последних цифр равны.
# !!!P.S.: функция не должна НИЧЕГО print'ить

def lucky_ticket(ticket_number):
    first = str(ticket_number)[:len(str(ticket_number)) // 2]
    second = str(ticket_number)[len(str(ticket_number)) // 2:]

    first_sum = sum(map(int, first))
    second_sum = sum(map(int, second))

    return first_sum == second_sum


print(lucky_ticket(123006))
print(lucky_ticket(12321))
print(lucky_ticket(436751))
