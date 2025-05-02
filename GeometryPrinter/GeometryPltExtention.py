import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols, solve
from sympy.geometry import Point, Segment, Line, Circle

# Point
def plot_point(point: Point, color=None, label=None, zorder=0, name=None, textcoords_name="offset points",
               xytext_name=(10, 10), ha_name='left'):
    """
    Параметры метода построения Точки класса Point на плоскости
    * point - объект класса sympy.geometry.Point (двухмерный)
    * color - цвет точки
    * label - подпись точки в легенде
    * zorder - число, объекты с большим значением zorder отображаются поверх объектов с меньшим значением,
    по умолчанию 0
    * name - подпись у объекта на плоскости
        # textcoords_name - смещение подписи относительно точки
        # xytext_name - смещение (по x и y)
        # ha_name - горизонтальное выравнивание ('left', 'right', 'center')
    """
    # Получаем координаты точки
    x, y = point.args

    # Отображаем точку
    plt.scatter(x, y, color=color, label=label, zorder=zorder)
    if name is not None:
        plt.annotate(name,
                     (x, y),
                     textcoords=textcoords_name,
                     xytext=xytext_name,
                     ha=ha_name)


# Segment
def plot_segment(segment: Segment, color=None, label=None,
                 zorder=0, ends_is_show=False, color_ends=None):
    """
    Параметры метода построения отрезка класса Segment на плоскости
    * segment - объект класса sympy.geometry.Segment (двухмерный)
    * color - цвет отрезка
    * label - подпись отрезка в легенде
    * zoder - число, объекты с большим значением zorder отображаются
    поверх объектов с меньшим значением, по умолчанию 0
    * ends_is_show - bool переменная которая отвечат за то будут ли
    изображаться концы отрезков
    * color_ends - цвет концов отрезка (будет применяться если ends_is_show=True)
    """
    # Получаем координаты концов отрезка
    x1, y1 = segment.p1.args
    x2, y2 = segment.p2.args

    # Отображаем отрезок
    plt.plot([x1, x2], [y1, y2], color=color, label=label, zorder=zorder)

    if ends_is_show:
        # Отображаем концы отрезка
        plt.scatter([x1, x2], [y1, y2], color=color_ends, zorder=zorder + 1)


# Line
def plot_line(line: Line, color=None, label=None, zorder=0):
    """
    Важно что метод plot_line можно использовать только
    после определения plt.xlim
    Параметры метода построения прямой класса Line на плоскости
    * line - объект класса sympy.geometry.Line (двухмерный)
    * color - цвет прямой
    * label - подпись прямой в легенде
    * zoder - число, объекты с большим значением zorder отображаются
    поверх объектов с меньшим значением, по умолчанию 0
    """
    # Определяем символические переменные
    x_min, x_max = plt.xlim()
    # Задаем пределы для оси x
    x_vals = [x for x in range(int(x_min) - 1, int(x_max) + 2)]

    # Определяем уравнение прямой A * x + B * y + C = 0
    x, y = symbols('x y')
    A, B, C = line.equation().as_coefficients_dict().values()
    eq_line = A * x + B * y + C
    solution = solve(eq_line, y)[0]

    # Подставляем значения x в уравнение прямой для нахождения y
    y_vals = [solution.subs(x, val) for val in x_vals]  # Подставляем x и находим y

    # Отображаем прямую
    plt.plot(x_vals, y_vals, label=label, color=color, zorder=zorder)


# Circle
def plot_circle(circle: Circle, color=None, label=None, zorder=0,
                center_is_show=False):
    """
    Параметры метода построения окружности класса Circle на плоскости
    * сircle - объект класса sympy.geometry.Circle (двухмерный)
    * color - цвет окружности
    * label - подпись окружности в легенде
    * zoder - число, объекты с большим значением zorder отображаются
    поверх объектов с меньшим значением, по умолчанию 0
    * center_is_show - bool аргумент отвечающий за изображение центра окружнности
    """
    # Создаем окружность с указанным центром и радиусом
    center = circle.center
    radius = circle.radius
    # Получаем координаты окружности
    theta = np.linspace(0, 2 * np.pi, 100)  # Угол в радианах для 100 точек
    x = center[0] + radius * np.cos(theta)  # Координаты x
    y = center[1] + radius * np.sin(theta)  # Координаты y

    plt.plot(x, y, color=color, label=label, zorder=zorder)
    if center_is_show:
        plt.scatter(*center, color=color, marker='o', zorder=zorder)


# Polygon
def plot_polygon(figure, color=None, label=None, is_fill=False,
                 zorder=0, vertices_is_show=False, vertices_color=None):
    # Разделяем координаты вершин
    x, y = zip(*figure.vertices)
    x = list(x) + [x[0]]
    y = list(y) + [y[0]]
    marker = None
    if is_fill:
        plt.fill(x, y, alpha=0.3)  # Заливка многоугольника

    if vertices_is_show and vertices_color is not None:
        plt.scatter(x, y, color=vertices_color, zorder=zorder + 1)
    if vertices_is_show:
        marker = 'o'
    plt.plot(x, y, marker=marker, label=label, color=color, zorder=zorder)
