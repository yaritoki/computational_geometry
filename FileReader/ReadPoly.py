import numpy as np
def read_poly(file_name):
    """
    Простой считыватель поли-файлов,
    который создает словарь Python с информацией о вершинах, ребрах и отверстиях.
    Предполагается, что вершины не имеют атрибутов или маркеров границ.
    Предполагается, что ребра не имеют маркеров границ.
    Региональные атрибуты или ограничения области не анализируются.
    """

    output = {'vertices': None, 'holes': None, 'segments': None}

    # открыть файл и сохранить строки в списке
    file = open(file_name, 'r')
    lines = file.readlines()
    file.close()
    lines = [x.strip('\n').split() for x in lines]

    # массив вершин
    vertices= []
    N_vertices, dimension, attr, bdry_markers = [int(x) for x in lines[0]]
    # Мы предполагаем, что attr = bdrt_markers = 0
    for k in range(N_vertices):
        label, x, y = [items for items in lines[k+1]]
        vertices.append([float(x), float(y)])

    output['vertices'] = np.array(vertices)

    # массив сегментов
    segments = []
    N_segments, bdry_markers = [int(x) for x in lines[N_vertices+1]]
    for k in range(N_segments):
        label, pointer_1, pointer_2 = [items for items in lines[N_vertices+k+2]]
        segments.append([int(pointer_1)-1, int(pointer_2)-1])

    output['segments'] = np.array(segments)

    # массив отверстий
    N_holes = int(lines[N_segments+N_vertices+2][0])
    holes = []
    for k in range(N_holes):
        label, x, y = [items for items in lines[N_segments + N_vertices + 3 + k]]
        holes.append([float(x), float(y)])

    output['holes'] = np.array(holes)

    return output