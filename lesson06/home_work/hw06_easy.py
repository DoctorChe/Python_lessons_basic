# Задача-1: Написать класс для фигуры-треугольника, заданного координатами трех точек.
# Определить методы, позволяющие вычислить: площадь, высоту и периметр фигуры.


class Point:
    """
    .p              p(x, y)
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    """
    p1------p2      p1(x, y)  p2(x, y)  y = k*x + b
    """
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    @property
    def length(self):
        return ((self.p2.x - self.p1.x) ** 2 + (self.p2.y - self.p1.y) ** 2) ** 0.5

    @property
    def k(self):
        return (self.p2.y - self.p1.y) / (self.p2.x - self.p1.x) if self.p2.x - self.p1.x != 0 else float("inf")


class Triangle:
    """
        p2         p1(x1, y1)      a  ->  y = a.k*x + a.b
       /  \        p2(x2, y2)      b  ->  y = b.k*x + b.b
      c    b       p3(x3, y3)      c  ->  y = c.k*x + c.b
     /      \
    p1--a---p2
    """
    def __init__(self, *args):
        self.p1 = args[0]
        self.p2 = args[1]
        self.p3 = args[2]
        self.a = Line(self.p1, self.p2)
        self.b = Line(self.p2, self.p3)
        self.c = Line(self.p3, self.p1)

    def area(self):
        p = self.perimeter() / 2  # полупериметр
        return (p * (p - self.a.length) * (p - self.b.length) * (p - self.c.length))**0.5

    def perimeter(self):
        return self.a.length + self.b.length + self.c.length

    def hight(self):
        h1 = 2 * self.area() / self.a.length
        h2 = 2 * self.area() / self.b.length
        h3 = 2 * self.area() / self.c.length
        return min(h1, h2, h3)


triangle = Triangle(Point(0, 0), Point(3, 0), Point(2, 3))
print(f"Площадь треугольника = {triangle.area():.3f}")
print(f"Периметр треугольника = {triangle.perimeter():.3f}")
print(f"Высота треугольника = {triangle.hight():.3f}")
print()

# Задача-2: Написать Класс "Равнобочная трапеция", заданной координатами 4-х точек.
# Предусмотреть в классе методы:
# проверка, является ли фигура равнобочной трапецией;
# вычисления: длины сторон, периметр, площадь.


class Trapeze:
    """
        p4---c---p3         p1(x, y)      a  ->  y = a.k*x + a.b
       /           \        p2(x, y)      b  ->  y = b.k*x + b.b
      d             b       p3(x, y)      c  ->  y = c.k*x + c.b
     /               \      p4(x, y)      d  ->  y = d.k*x + d.b
    p1-------a-------p2
    """
    def __init__(self, *args):
        self.p1 = args[0]
        self.p2 = args[1]
        self.p3 = args[2]
        self.p4 = args[3]
        self.a = Line(self.p1, self.p2)
        self.b = Line(self.p2, self.p3)
        self.c = Line(self.p3, self.p4)
        self.d = Line(self.p4, self.p1)

    def is_trapeze(self):
        if self.a.k == self.c.k and self.b.length == self.d.length:
            return True
        elif self.b.k == self.d.k and self.a.length == self.c.length:
            return True
        else:
            return False

    def area(self):
        return (self.a.length + self.c.length) / 2 * (self.d.length**2 - (self.a.length - self.c.length)**2 / 4)**0.5

    def perimeter(self):
        return self.a.length + self.b.length + self.c.length + self.d.length

    def hight(self):
        if self.a.k == self.c.k:
            h = 2 * self.area() / (self.a.length + self.c.length)
        else:
            h = 2 * self.area() / (self.b.length + self.d.length)
        return h


trapeze1 = Trapeze(Point(0, 0), Point(3, 0), Point(2, 2), Point(1, 2))
print(trapeze1.is_trapeze())
print(f"Площадь трапеции = {trapeze1.area():.3f}")
print(f"Периметр трапеции = {trapeze1.perimeter():.3f}")
print(f"Высота трапеции = {trapeze1.hight():.3f}")
print()

trapeze2 = Trapeze(Point(0, 0), Point(3, 0), Point(5.5, 2), Point(1, 2))
print(trapeze2.is_trapeze())
print()

trapeze3 = Trapeze(Point(0, 0), Point(0, -3), Point(2, -2), Point(2, -1))
print(trapeze3.is_trapeze())
print()
