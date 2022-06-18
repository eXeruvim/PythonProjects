
#
# Выполнили:
#   Черняев Андрей, Карманов Сергей
#

import csv
from random import randint
import operator

# Нормализация параметров методом "минимакс"
def normalize(item, min_list, max_list):
    for i in range(0, 4):
        item[i] = (item[i] - min_list[i]) / (max_list[i] - min_list[i])

# Расчёт Манхэттенского расстояния
def calc_distance(item1, item2):
    distance = 0
    for i in range(0, 4):
        distance += abs(item1[i] - item2[i])
    return distance

# Заполнение списка начальными данными
iris_data = []
with open('iris.csv', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        for i in range(0, 4):
            row[i] = float(row[i])
        iris_data.append(row)

testing_data = []

# Случайный выбор тестового набора данных и их удаление из начального набора
for i in range(0, 50):
    index = randint(0, len(iris_data)-1)
    testing_data.append(iris_data.pop(index))

# Поиск минимальных и максимальных значений параметров тренировочного набора
min_list = iris_data[0][0:4]
max_list = iris_data[0][0:4]
for i in range(0, 4):
    for item in iris_data:
        if min_list[i] > item[i]:
            min_list[i] = item[i]
        if max_list[i] < item[i]:
            max_list[i] = item[i]

# Нормализация
for item in iris_data:
    normalize(item, min_list, max_list)

k = int(input("Укажите параметр k: "))

# Переменная для подсчета точности
correct = 0

# Блок классификации
for test_item in testing_data:
    # Нормализация
    normalize(test_item, min_list, max_list)
    # Расчёт расстояний
    distance_list = []
    for index in range(0, len(iris_data)):
        distance = calc_distance(test_item, iris_data[index])
        distance_list.append((index, distance))
    # Сортировка списка расстояний по возрастанию
    distance_list.sort(key=operator.itemgetter(1))
    # Выбор k соседей с наименьшим расстоянием
    neighbours = [distance_list[i][0] for i in range(0, k)]

    # Определение классов соседей
    class_list = []
    count_list = []
    for i in neighbours:
        if not iris_data[i][4] in class_list:
            class_list.append(iris_data[i][4])
            count_list.append(0)

    # Подсчёт количества соседей каждого класса
    for i in neighbours:
        for j in range(0, len(class_list)):
            if iris_data[i][4] == class_list[j]:
                count_list[j] += 1

    # Выбор класса, к которому принадлежат большинство соседей
    index = count_list.index(max(count_list))
    test_item.append(class_list[index])

    # Вывод результатов классификации
    if test_item[4] == test_item[5]:
        print("ВЕРНО!")
        correct += 1
    else:
        print("НЕВЕРНО!")
    print("Сорт", test_item[4], " определен как", test_item[5], '\n')

# Подсчёт точности
print("Точность классификации составила", correct / len(testing_data) * 100,"%")
