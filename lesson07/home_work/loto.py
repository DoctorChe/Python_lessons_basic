#!/usr/bin/python3

"""
== Лото ==

Правила игры в лото.

Игра ведется с помощью специальных карточек, на которых отмечены числа, 
и фишек (бочонков) с цифрами.

Количество бочонков — 90 штук (с цифрами от 1 до 90).

Каждая карточка содержит 3 строки по 9 клеток. В каждой строке по 5 случайных цифр, 
расположенных по возрастанию. Все цифры в карточке уникальны. Пример карточки:

--------------------------
    9 43 62          74 90
 2    27    75 78    82
   41 56 63     76      86 
--------------------------

В игре 2 игрока: пользователь и компьютер. Каждому в начале выдается 
случайная карточка. 

Каждый ход выбирается один случайный бочонок и выводится на экран.
Также выводятся карточка игрока и карточка компьютера.

Пользователю предлагается зачеркнуть цифру на карточке или продолжить.
Если игрок выбрал "зачеркнуть":
	Если цифра есть на карточке - она зачеркивается и игра продолжается.
	Если цифры на карточке нет - игрок проигрывает и игра завершается.
Если игрок выбрал "продолжить":
	Если цифра есть на карточке - игрок проигрывает и игра завершается.
	Если цифры на карточке нет - игра продолжается.
	
Побеждает тот, кто первый закроет все числа на своей карточке.

Пример одного хода:

Новый бочонок: 70 (осталось 76)
------ Ваша карточка -----
 6  7          49    57 58
   14 26     -    78    85
23 33    38    48    71   
--------------------------
-- Карточка компьютера ---
 7 87     - 14    11      
      16 49    55 88    77    
   15 20     -       76  -
--------------------------
Зачеркнуть цифру? (y/n)

Подсказка: каждый следующий случайный бочонок из мешка удобно получать 
с помощью функции-генератора.

Подсказка: для работы с псевдослучайными числами удобно использовать 
модуль random: http://docs.python.org/3/library/random.html

"""
import random


class Draw:
    def __init__(self):
        self.draw = []
        self.clean = self.draw.count(-1) == 15

    def new_draw(self):
        seq = random.sample(range(1, 91), k=15)
        line1 = self.new_line(seq[0:5])
        line2 = self.new_line(seq[5:10])
        line3 = self.new_line(seq[10:15])
        self.draw = line1 + line2 + line3

    @staticmethod
    def new_line(line):
        line.sort()
        line.insert(random.randint(0, 5), 0)
        line.insert(random.randint(0, 6), 0)
        line.insert(random.randint(0, 7), 0)
        line.insert(random.randint(0, 8), 0)
        return line

    @staticmethod
    def print_line(line):
        new_line = ""
        for number in line:
            if number == -1:
                number = '-'
            if number == 0:
                number = ''
            new_line += str(number) + "\t"
        return new_line

    def print_draw(self):
        print(self.print_line(self.draw[0:9]))
        print(self.print_line(self.draw[9:18]))
        print(self.print_line(self.draw[18:27]))

    def check_number(self, number):
        if number in self.draw:
            index = self.draw.index(number)
            self.draw.pop(index)
            self.draw.insert(index, -1)
            return True
        return False


class Player:
    def __init__(self, name):
        self.name = name
        self.draw = Draw()

    def take_draw(self):
        self.draw.new_draw()

    def check_draw(self, number):
        return self.draw.check_number(number)

    def print_draw(self):
        self.draw.print_draw()


class You(Player):

    def __init__(self, name="Игрок"):
        your_name = input("Введите ваше имя")
        if your_name:
            name = your_name
        Player.__init__(self, name)
        print(f"Добро пожаловать в игру {self.name}")

    def print_draw(self):
        print("---------- Ваша карточка ---------")
        self.draw.print_draw()
        print("----------------------------------")


class Computer(Player):

    def __init__(self, name="Компьютер"):
        Player.__init__(self, name)

    def print_draw(self):
        print("------- Карточка компьютера ------")
        self.draw.print_draw()
        print("----------------------------------")


class Lotto:
    def __init__(self):
        self.player = You()
        self.comp = Computer()
        self.barrels = []
        self.game = True

    def start_game(self):
        self.player.take_draw()
        self.player.print_draw()
        self.comp.take_draw()
        self.comp.print_draw()
        self.generate_barrels()

    def generate_barrels(self):
        barrels = [x for x in range(1, 91)]
        random.shuffle(barrels)
        self.barrels = barrels

    def play_round(self):
        number = self.barrels.pop()
        print(f"Новый бочонок: {number} (осталось {len(self.barrels)})")
        take_barrel = input("Зачеркнуть цифру? (y/n)").lower() == 'y'
        if take_barrel:
            if self.player.check_draw(number):
                print("Вы зачеркнули цифру")
            else:
                print("Вы проиграли, нет такой цифры на поле")
                self.game = False
        else:
            print("Вы пропустили ход")
            if self.player.check_draw(number):
                print("Вы проиграли, на поле была такая цифра")
                self.game = False
        if self.comp.check_draw(number):
            print("Компьютер зачеркнул цифру")
        else:
            print("Компьютер пропустил ход")
        self.player.print_draw()
        self.comp.print_draw()
        if self.player.draw.clean:
            print("Вы выиграли")
            self.game = False
        if self.comp.draw.clean:
            print("Компьютер выиграл")
            self.game = False


game = Lotto()
game.start_game()
while game.game:
    game.play_round()
