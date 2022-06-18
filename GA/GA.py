import random

# Функция одноточечного скрещивания
def crossover(population, child_count, length):
    # Случайным образом выбираются 5 пар хромосом для скрещивания
    # Каждая пара формирует список из двух элементов, после чего все пары заносятся в список списков
    selected = [random.sample(population, 2) for i in range(child_count//2)]
    # Из списка поочередно выбираются пары для последующего скрещивания
    for list in selected:
        # Случайным образом определяется точка скрещивания
        l = random.randint(1, length - 2)
        # В список популяций добавляются потомки, полученные в ходе одноточечного скрещивания
        population.append(list[0][:l] + list[1][l:])
        population.append(list[1][:l] + list[0][l:])
    return population

# Функция мутации обменом
def mutation(population, mutation_probability):
    for list in population:
        # Если вероятность мутации больше случайного значения
        if mutation_probability > random.random():
            # Случайным образом выбираются два бита
            i = random.randint(0, len(list) - 1)
            j = random.randint(0, len(list) - 1)
            # Значение битов меняются местами
            list[i], list[j] = list[j], list[i]
    return population

# Функция редукции методом ранжированного отбора
def reduction(population, fit_func, result_count):
    # Запись отсортированных по возрастанию значений фитнес-функции в список
    sort_fit = sorted(fit_func)
    # Инициализация списка для хранения рангов
    ranks = []
    # В цикле сопоставляются значения фитнес-функции со значениями отсортированной фитнес-функции
    for i in range(0, len(fit_func)):
        for j in range(0, len(sort_fit)):
            # Если значение совпало
            if fit_func[i] == sort_fit[j]:
                # то в список рангов добавляется индекс элемента отсортированной фитнес-функции
                ranks.append(j+1)
                # Значение отсортированной фитнес-функции перезаписывается большим числом для того, чтобы исключить
                # его из дальнейшего поиска
                sort_fit[j] = 1000
                break
    # Расчитывается сумма рангов
    sum_ranks = sum(ranks)
    # Список рангов перезаписывается долями рангов
    ranks = [ranks[i] / sum_ranks for i in range (len(ranks))]

    # Инициализация списка границ секторов
    borders = []
    border = 0
    # Заполнение списка границ накопительными суммами
    for i in ranks:
        border = border + i
        borders.append(border)

    # Инициализация множества для хранения результата
    result = set()
    # Цикл с условием для отбора 20 хромосом
    while len(result) != result_count:
        # Случайным образом генерируется число в диапазоне от 0 до 1
        select = random.random()
        # Нахождение интервала, в котором находится случайное число
        for j in range(0, len(population)):
            if select < borders[j]:
                # Добавление индекса хромосомы во множество
                result.add(j)
                break
    return result



def main():

    # Значения по умолчанию
    length = 30
    initial_count = 20
    result_count = 20
    child_count = 10

    answer = input('Использовать данные по умолчанию или нет (Y/N): ')
    if answer.upper() == 'N':
        length = int(input('Длина одной хромосомы: '))
        initial_count = int(input('Начальное количество хромосом: '))
        child_count = int(input('Количество потомков: '))
        result_count = int(input('Количество хромосом после редукции: '))

    # Создание начальной популяции
    # Случайная генерация 20 хромосом по 30 бит каждая
    # Сгенерированные хромосомы заносятся в список списков population
    population = [[random.randint(0, 1) for i in range(length)] for j in range(initial_count)]

    # Случайным образом определяется вероятность мутации
    mutation_probability = random.uniform(0.1, 0.3)

    # Скрещивание
    population = crossover(population, child_count, length)

    # Подсчет фитнес-функции
    fit_func = [sum(i) for i in population]

    # Мутация
    population = mutation(population, mutation_probability)

    # Редукция
    result = reduction(population, fit_func, result_count)

    # Вывод
    print('\nХромосомы, оставшиеся после редукции: ')
    for i in result:
        print('\nХромосома №', i+1)
        print(population[i])

main()
