import sys
import numpy as np
import random as rn
from numpy.random import choice as np_choice

# Объявление класса для муравьиного алгоритм
# Через классы проще реализовать, чем процедурно
class AntAlgorithm(object):
	# Вызов инициализаци
	def __init__(self, distances, num_ants, num_interations, evaporation, alpha, beta):
		self.distances = distances										# Матрица расстояний
		self.pheromone = np.ones(self.distances.shape) / len(distances)	# Матрица феромонов
		self.all_vertices = range(len(distances))						# Все вершины графа
		self.num_ants = num_ants										# Количество муравьёв
		self.num_interations = num_interations							# Кол-во интераций
		self.evaporation = evaporation									# Коэффициент испарения
		self.alpha = alpha												# alpha	(float)
		self.beta = beta												# betta	(float)

    # Главная функция
	def run(self):
		shortest_way = None	# Объявление переменной для кратчайшего пути
		all_time_shortest_way = ("route", np.inf)	# Матрица с путями
		for i in range(self.num_interations):
			all_route = self.gen_all_route()	# Заполнение матрицы всеми маршрутами
			self.distribution_pheromone(all_route, self.num_ants, shortest_way=shortest_way) # Добавление феромонов на маршруты
			shortest_way = min(all_route, key=lambda x: x[1])	# Поиск кратчайших путей

			if (shortest_way[1] < all_time_shortest_way[1]):	#Нахождение самого короткого пути
				all_time_shortest_way = shortest_way
			self.pheromone * self.evaporation			#Испарение феромонов
			print("Итерация №", i, "\nРасстояние:", all_time_shortest_way[1])
		return all_time_shortest_way[1] # !!! Чтобы полностью увидеть путь, нужно убрать [1]

	# Добавление феромонов на пройденные участки
	def distribution_pheromone(self, all_route, num_ants, shortest_way):
		sorted_way = sorted(all_route, key=lambda x: x[1])		# Все маршруты муравьёв в этой итерации, количество муравьёв, кротчайший путь
		for way, dist in sorted_way[:num_ants]:
			for move in way:
				self.pheromone[move] += 1/self.distances[move]

	# Подсчет длины пути муравья
	def gen_path_dist(self, way):
		total_distance = 0	# Переменная для длины маршрута
		for l in way:
			 total_distance += self.distances[l] # Подсчет длины маршрута
		return total_distance	# Длина маршрута

	# Маршруты всех муравёв
	def gen_all_route(self):
		all_route = []	# Массив для всех маршрутов
		for i in range(self.num_ants):
			way = self.gen_way(0) # Вершина отправления
			# Раскомментировать, чтобы вершина отправления для каждого муравья выбиралась рандомно
			#way = self.gen_way(rn.randrange(0, len(self.distances)))
			all_route.append((way, self.gen_path_dist(way))) # Добавление в массив вершину и путь от нее
		return all_route				# Список маршрутов всех муравьёв и его длина

	# Муршрут каждого муравья
	def gen_way(self, start):
		way = []	# Маршруты муравья
		visited = set() # Места, которые посетил муравей
		visited.add(start)	# Начальная позиция
		tmp = start
		for i in range(len(self.distances)-1):
			move = self.pick_move(self.pheromone[tmp], self.distances[tmp], visited) # Передвижение
			way.append((tmp, move))
			tmp = move
			visited.add(move)	# Отмечаем посещенные места
		way.append((tmp, start))	# Возврат в начальную точку
		return way				# Список маршрута муравья

	# Функция выбора следующей вершины
	# Параметры: Массив феромонов в следующие вершины, Массив расстояний до след вершин, кортеж с первой вершиной)
	def pick_move(self, pheromone, dist, visited):
		pheromone = np.copy(pheromone)
		pheromone[list(visited)] = 0

		choice = pheromone ** self.alpha * ((1.0/dist) ** self.beta)	# Вероятность перехода из вершины i в вершину j

		norm_choice = choice / choice.sum()		# Нормирование

		move = np_choice(self.all_vertices, 1, p=norm_choice) [0]		# Выбор маршрута
		return move

#Входные данные
data = []
f = open('byes29.tsp', 'r')
for line in f:
    data.append([int(x) for x in line.split()])
distances = np.array(data)

i, j = 0, 0
#изменнение главное диагонали, чтобы нельзя было пройти из города в тот же город
for p in range(len(distances)):
	distances[i][j] = 9999
	i+=1
	j+=1

antN, iterN, evoC, alpha, beta = 12, 100, 0.15, 1, 2
print(
'Численность колонии муравьев:', antN,
'\nКоличество итераций:', iterN,
'\nКоэффициент испарения феромонов:', evoC,
'\nАльфа:', alpha, '\nБета: ', beta)

vote = input('Использовать параметры по умолчанию? (Y/N): ')
if vote == 'N' or vote == 'n':
	antN = int(input("Численность колонии муравьев: "))
	iterN = int(input("Количество итераций: "))
	evoC = float(input("Коэффициент испарения феромонов: "))
	alpha = float(input("Альфа: "))
	beta = float(input("Бета: "))

ant_algorithm = AntAlgorithm(distances, antN, iterN, evoC, alpha, beta)	# Создание экземпляра класса
shortest_path = ant_algorithm.run()		# Запуск главной функции
print("Самый короткий путь:", str(shortest_path))
