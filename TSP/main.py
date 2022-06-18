import random

# Выполнили:
#   Черняев Андрей, Карманов Сергей

# Процедура для вывода маршрута
def distance(routes):
    # Данные взяты из файла byes29 из бенчмарков
    # Данные будут храниться в списке списков data
    data = []
    f = open('byes29.tsp', 'r')
    for line in f:
        data.append([int(x) for x in line.split()])

    # Подсчёт длины
    length = [0 for i in range(len(routes))]
    for j in range(len(routes)):
        for i in range(len(routes[j])):
            length[j] += data[routes[j][i]][routes[j][(i+1) % len(routes[j])]]
    # Вывод длин
    print()
    for i in range(len(length)):
        print('Длина маршрута №', i+1, length[i])



# Количество пунктов
n = 20
# Создание списка, в котором хранятся списки, содержащие маршруты [0, 1, 2, .., 18, 19]
routes = [[i for i in range(n)] for j in range(2)]
# Перемешивание пунктов в маршрутах
for item in routes:
    random.shuffle(item)

# Случайный выбор пункта в маршрутах
point = random.randint(0, n-1)
# Нахождение индексов выбранного пункта
index = [item.index(point) for item in routes]

# Список для хранения результирующего маршрута
child = [point]
# Флаги для проверки возможности выбора пункта из маршрута
f_is_not_over, s_is_not_over = True, True
# Скрещивание
while f_is_not_over or s_is_not_over:
    # Уменьшение индекса выбранного пункта первого маршрута на 1
    index[0] = (index[0] - 1) % n
    # Увеличение индекса выбранного пункта второго маршрута на 1
    index[1] = (index[1] + 1) % n
    # Если пункт в первом маршруте выбрать можно
    if f_is_not_over:
        # Если пункта нет в результирующем маршруте
        if routes[0][index[0]] not in child:
            # То добавить пункт в начало
            child.insert(0, routes[0][index[0]])
        else:
            # Иначе сделать возможность выбора недоступной
            f_is_not_over = False
    # Если пункт во втором маршруте выбрать можно
    if s_is_not_over:
        # Если пункта нет в результирующем маршруте
        if routes[1][index[1]] not in child:
            # То добавить пункт в конец
            child.append(routes[1][index[1]])
        else:
            # Иначе сделать возможность выбора недоступной
            s_is_not_over = False

# Если длина результирующего маршрута не равна длине маршрута родителя
if len(child) != len(routes):
    # Запись недостающих пунктов в результатирующий список
    for item in routes[0]:
        if item not in child:
            child.append(item)

# Вывод
for i in range(2):
    print('Маршрут №', i+1, routes[i])
print('Выбранный элемент:', point)
print('Результат: ', child)

# Вывод длин маршрутов
routes.append(child)
distance(routes)
