# Разработать программу для вычисления кратчайшего пути для почтальона.
# Описание задачи
# Почтальон выходит из почтового отделения, объезжает всех адресатов один раз для вручения посылки и возвращается в
# почтовое отделение.
# Необходимо найти кратчайший маршрут для почтальона.
# Координаты точек
# Почтовое отделение – (0, 2)
# Ул. Грибоедова, 104/25 – (2, 5)
# Ул. Бейкер стрит, 221б – (5, 2)
# Ул. Большая Садовая, 302-бис – (6, 6)
# Вечнозелёная Аллея, 742 – (8, 3)

from math import sqrt


def calc_dist(first_point: tuple, second_point: tuple) -> float:
    '''
    Функция расчета расстояния между двумя точками
    :param first_point: координаты первой точки
    :param second_point: координаты второй точки
    :return: число типа float
    '''
    x1, y1 = first_point
    x2, y2 = second_point
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def short_path() -> dict:
    '''
    Функция находт блжайшую точку извлекает её из списка и добавляет в словарь расстояние, координыты начальной и
    конечной точек
    :return:
    Словарь вида - {(начальная точка, конечная точка): расстояние между точками}
    '''
    ls_point = [(2, 5), (5, 2), (6, 6), (8, 3)]
    dict_dist = dict()
    begin, end = (0, 2), 0
    while len(ls_point):
        dist = calc_dist(begin, ls_point[0])
        for sym in ls_point:
            calc = calc_dist(begin, sym)
            if calc <= dist:
                dist, end = calc, sym
        dict_dist[begin, end] = dist
        begin = ls_point.pop(ls_point.index(end))
    dict_dist[end, (0, 2)] = calc_dist(end, (0, 2))
    return dict_dist


def data_output(dict_dist:dict) -> None:
    '''
    Функция вывода
    :param dict_dist: Словарь вида - {(начальная точка, конечная точка): расстояние между точками}
    :return: None
    '''
    dict_point = {(0, 2): 'Почтовое отделение', (2, 5): 'Ул. Грибоедова, 104/25', (5, 2): 'Ул. Бейкер стрит, 221б',
                  (6, 6): 'Ул. Большая Садовая, 302-бис', (8, 3): 'Вечнозелёная Аллея, 742'}
    width = 30
    total = 0
    header = "Начальая точка".center(39) + "Конечая точка".center(42) + "Растояние"
    print(header)
    for pair, distance in dict_dist.items():
        print(f'{dict_point[pair[0]]:{width}} - {pair[0]}|{dict_point[pair[1]]:{width}} - {pair[1]}| {distance:.3f}')
        total += distance
    print()
    print(f'Общая продолжительность пути: {total: .3f}')
    return None

def output_like_task(dict_dist:dict) -> None:
    '''
    Функция вывода как представленно в задании
    :param dict_dist: Словарь вида - {(начальная точка, конечная точка): расстояние между точками}
    '''
    total = 0
    string = '(2, 0)'
    for pair, distance in dict_dist.items():
        string += f' -> {pair[1]}[{distance}]'
        total += distance
    print()
    print('Вывод как в задании:')
    print(f'{string} = {total}')
    return None


data_output(short_path())
output_like_task(short_path())








