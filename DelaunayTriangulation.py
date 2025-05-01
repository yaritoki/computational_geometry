from matplotlib import pyplot as plt
from sympy.geometry import Point, Polygon, Segment
from DataStructure.Node import Node
from DataStructure.Triangle import Triangle
from itertools import combinations

from GeometryPrinter.GeometryPltExtention import plot_polygon, plot_point, plot_segment, plot_circle


class DelaunayTriangulation:
    def __init__(self, polygon: Polygon):
        self.triangles = self.triangulate_polygon(polygon)
        self.nodes = []
        for point in polygon.vertices:
            self.add_point(point)

    def add_point(self, point: Point):
        new_node = Node(point)
        self.nodes.append(new_node)

        # Находим треугольники, описанные вокруг нового узла
        triangles_to_remove = []
        for triangle in self.triangles:
            if triangle.contains(point):
                triangles_to_remove.append(triangle)

        self.remove_triangles(triangles_to_remove)
        self.form_new_triangles(new_node, triangles_to_remove)

    def remove_triangles(self, triangles: Triangle):
        for triangle in triangles:
            self.triangles.remove(triangle)

    def form_new_triangles(self, new_node: Node, removed_triangles):
        # Формируем новый треугольник, соединяя новый узел с контурами удалённых треугольников
        if not removed_triangles:
            return

        polygon_points = []
        for triangle in removed_triangles:
            polygon_points.extend(triangle.points)

        unique_points = list(set(tuple(p) for p in polygon_points))
        # Создаем новый треугольник для каждого ребра контура
        for i in range(len(unique_points)):
            p1 = unique_points[i]
            p2 = unique_points[(i + 1) % len(unique_points)]
            new_triangle = Triangle(p1, p2, new_node.point)
            self.triangles.append(new_triangle)

    def triangulate(self, polygon: Polygon):

        for point in polygon.vertices:
            self.add_point(point)

    def get_diagonals(self, polygon: Polygon):
        # Получаем список вершин многоугольника
        vertices = polygon.vertices
        n = len(vertices)
        diagonals = []

        # Перебираем все возможные пары вершин
        for i in range(n):
            for j in range(i + 2, n - (i == 0)):
                # Создаем отрезок между вершинами i и j
                segment = Segment(vertices[i], vertices[j])
                diagonals.append(segment)

        return diagonals

    def find_intersections(self, diagonals):
        """Найти все пересечения диагоналей."""
        intersections = set()
        for d1, d2 in combinations(diagonals, 2):
            intersection = d1.intersection(d2)
            for point in intersection:
                intersections.add(point)
        return list(intersections)

    def is_point_inside_circumcircle(self, triangle: Triangle, point: Point):
        """
        Проверяет, находится ли точка внутри описанной окружности треугольника.
        """
        circle = triangle.circumcircle
        if circle is None:
            return False  # Точки коллинеарны, окружность не существует
        return circle.encloses(point)

    def is_triangle_valid(self, triangle, points):
        """
        Проверяет, является ли треугольник допустимым (никакая другая точка не находится внутри его описанной окружности).
        """
        for p in points:
            if p not in triangle.vertices and self.is_point_inside_circumcircle(triangle, p):
                return False
        return True

    def triangulate(self, points):
        """
        Триангуляция набора точек методом перебора.
        Возвращает список треугольников (sympy.geometry.Polygon).
        """
        triangles = []

        # Перебираем все возможные комбинации из 3 точек
        for triplet in combinations(points, 3):
            triangle = Polygon(*triplet)

            if len(triangle.args) != 3:
                continue  # Пропускаем вырожденные треугольники

            # Проверяем, что треугольник не вырожденный (площадь > 0)
            if triangle.area == 0:
                continue  # Пропускаем вырожденные треугольники

            # Проверяем, что треугольник допустим (никакая другая точка не внутри его описанной окружности)
            if self.is_triangle_valid(triangle, points):
                triangles.append(triangle)

        return triangles

    def triangulate_polygon(self, polygon: Polygon):
        """Триангулировать многоугольник, используя его диагонали."""
        if len(polygon.vertices) < 3:
            return []  # Не может быть треугольников в многоугольнике с 0-2 вершинами

        # Получаем все диагонали многоугольника
        diagonals = self.get_diagonals(polygon)
        # Находим все пересечения диагоналей
        intersection_points = self.find_intersections(diagonals)

        # Добавляем точки пересечения к вершинам многоугольника
        vertices = polygon.vertices + intersection_points

        # Создаем новый многоугольник из всех вершин
        # plt.figure(figsize=(10, 10))
        # plt.xlim(-1,3)
        # plt.ylim(-1,3)
        # plot_polygon(polygon, color='green')
        # for p in vertices:
        #     plot_point(p, color='blue')
        # plt.show()

        # Формируем треугольники с использованием вершины и отображаем (но не реализуем сложный алгоритм триангуляции)
        triangles = self.triangulate(vertices)
        # for t in triangles:
        #     plt.figure(figsize=(10, 10))
        #     plot_circle(t.circumcircle, color="g")
        #     plot_polygon(t, color='red')
        #     plt.show()
        return [Triangle(t.vertices) for t in triangles]