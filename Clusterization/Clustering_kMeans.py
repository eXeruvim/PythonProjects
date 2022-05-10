import random, csv, math
import numpy as np
from matplotlib import pyplot as plt

# По неизвестной причине программа 1 раз сломалась на стадии запуска,
# Поэтому, если это произошло, то следует просто перезапустить программу
# Причину я так и не смог обнаружить, скорее всего, неправильно были проинициализированы данные.


# Загрузка данных из файла .csv
def load_data(file):
    with open (file, 'r') as csvfile:
        dataset = csv.reader(csvfile)
        dataset = list(dataset)
        for x in range(len(dataset)):
            dataset[x] = dataset[x][:4]
            for y in range(len(dataset[0])):
                dataset[x][y] = float(dataset[x][y])
    return dataset

# Распределение ирисов по классам
def distribution(reader):
    class1 = [] # Контейнер для класса "Setosa"
    class2 = [] # Контейнер для класса "Versicolor"
    class3 = [] # Контейнер для класса "Virginica"
    structured_cluster = []
    with open(reader, 'r') as csvread:
        data = csv.reader(csvread)
        data = list(data)
        for i in range (len(data)):
            for j in range(len(data[i]) - 1):
                data[i][j] = float(data[i][j])
    # Поиск соответствующих классов
    for i in range(len(data)):
        if data[i][4] == 'Iris-setosa':
            class1.append(data[i][:4])
        elif data[i][4] == 'Iris-versicolor':
            class2.append(data[i][:4])
        elif data[i][4] == 'Iris-virginica':
            class3.append(data[i][:4])
    structured_cluster.append(class1)
    structured_cluster.append(class2)
    structured_cluster.append(class3)
    return structured_cluster

# Инициализация центроидов
def initialize_centrioid(data, clustersNum):
    centeroids = [] # Объявление листа для значения центроида
    rand = random.sample(range(len(data)), clustersNum * 2) # Рандом для центроида
    for i in rand:
            centeroids.append(dataset[i])
    return centeroids

# Создание нового центроида
def evaluating_new_centroid(clusters):
    temp = np.array(clusters, dtype=object) # Временная переменная
    new_centroid = []   # Лист для нового центроида
    for i in range(len(temp)):
        x = (np.average(temp[i],axis=0)) # Местоположение центроида по оси Х
        y = x.tolist()  # Местоположение центроида по оси У
        new_centroid.append(y) # Координаты центроида
    return (new_centroid)

# Вычисление расстояния Евклида / евклидово расстояние
def euclidian_distance(instance, centroid):
    summation = 0
    for attribute in range(len(instance)):
        summation += (instance[attribute] - centroid[attribute]) ** 2
    euclidian = math.sqrt(summation)
    return euclidian

# Главный метод - вычисление К-средних
def clustering(dataset, initialize_centrioid, K):
    length = len(initialize_centrioid) # Длина первоначального центроида
    new_centroid = initialize_centrioid[0:int(length / 2)] # Новый центроид
    prev_centroid = initialize_centrioid[int(length / 2):length] # Предыдущий центроид
    iteration = 0   # Счетчик
    while len([p for p in (new_centroid) if p not in prev_centroid])!= 0 and iteration < 100:
        clusters = [[] for i in range (0, K)] # Кластеры, которые будут привязаны к центроидам
        for i in range (len(dataset)):
            euclidian_metric = [] # Значение расстояния
            for j in range (len(new_centroid)):
                euclidian_metric.append(euclidian_distance(dataset[i], new_centroid[j])) # Вычисление расстояния
            cluster_value = np.argmin(np.array(euclidian_metric)) # Расстояние класстера до созданного до созданного центроида
            clusters[cluster_value].append(dataset[i]) # Заполненние кластеров данными
        prev_centroid = new_centroid    # После завершения манипуляций над созданным центроидом
        new_centroid = evaluating_new_centroid(clusters) # Создается новый центроид
        iteration += 1
    return clusters, new_centroid

# Отображение данных на графике
def visualization(clusters, K, centroid):
    x = [] # Координаты по Х
    y = [] # Координаты по У
    center_x = [] # Координаты центра Х
    center_y = [] # Координаты центра У
    center_label = [] # Центральная метка
    labels = []
    for i in range (len(centroid)):
        # Добавления центроида на график
        center_x.append(centroid[i][0])
        center_y.append(centroid[i][3])
        center_label.append(i)
        # Добавление кластеров возле него
    for i in range (len(clusters)):
        for j in range(len(clusters[i])):
            x.append(clusters[i][j][0])
            y.append(clusters[i][j][3])
            labels.append(i)
    # Цвета для кластеров и центроидов
    label_color_map = {0: 'r', 1: 'g', 2: 'b'}
    # Покраска кластеров
    label_color = [label_color_map[l] for l in labels]
    # Покраска центроидов
    center_label_color = [label_color_map[l] for l in center_label]
    # Отображение данных
    x = plt.scatter(x, y, s = 50, alpha = 0.7, c = label_color, label = 'Кластер')
    y = plt.scatter(center_x, center_y, s = 80, alpha = 1, c = center_label_color, marker = '*', label = 'Центроид')
    plt.legend(loc=2)
    plt.show()
    return x, y

# Вычисление точности работы алгоритма
# Обычно это 68(66) / 100 / 68(66), но иногда проскаивают и неожиданные результаты
def accuracy(cluster, structured_data):
    clusters = ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']
    accuracy_value = []
    for i in range (len(cluster)):
        temp = []
        for j in range(len(structured_data)):
            # Сложение суммы длин значений, которые не соответствуют изначальным данным
            temp.append(len([p for p in cluster[i] if p not in structured_data[j]]) + len([p for p in structured_data[j] if p not in cluster[i]]))
        # Поиск соответствий индексов минимальных значений по классам ирисов
        if np.argmin(np.array(temp)) == 0:
            classification='Iris-setosa'
        elif np.argmin(np.array(temp)) == 1:
            classification='Iris-versicolor'
        elif np.argmin(np.array(temp)) == 2:
            classification='Iris-virginica'
        # Подсчет точности в процентном соотношении. (Точность на кластер)
        accuracy_value.append(100 - ((float(temp[np.argmin(np.array(temp))]) / 50) * 100))
    # Отображение данных
    plt.bar(clusters, accuracy_value)
    plt.xlabel('Классы (кластеры)')
    plt.ylabel('Точность')
    plt.title('Точность в процентном соотношении')
    for i in range(len(clusters)):
        plt.text(clusters[i], accuracy_value[i] + 1, accuracy_value[i])
    plt.show()
#----------------------------------------------------------------------------------------------
# Инициализация и вызов функций
data = 'iris.csv'
dataset = load_data(data)
initialize_centrioid = initialize_centrioid(dataset, clustersNum = 3)
cluster = clustering(dataset, initialize_centrioid, K = 3)
visualization(cluster[0], 3, cluster[1])
structured_data = distribution(data)
accuracy(cluster[0], structured_data)
