


# Выполнили:
#   Черняев Андрей,
#   Карманов Сергей


# Класс для хранения вариантов погодных условий
class Line:

    def __init__(self, yes, no):
        self.yes = yes
        self.no = no
    # Задание вероятностей
    def set_probability(self, p_yes, p_no, p):
        self.p_yes = p_yes
        self.p_no = p_no
        self.p = p

# Класс для хранения погодных условий
class X:
    def __init__(self):
        self.lines = []
    # Задать значение для строки
    def add_line(self, line):
        self.lines.append(line)

    # Подсчет вероятностей
    def calculate_probabilities(self, sum_yes, sum_no):
        for line in self.lines:
            p_yes = line.yes / sum_yes
            p_no = line.no / sum_no
            p = (line.yes + line.no) / (sum_yes + sum_no)
            line.set_probability(p_yes, p_no, p)

# Цветной вывод
def out_red(text):
    print("\033[31m{}\033[0m" .format(text))

def out_green(text):
    print("\033[32m{}\033[0m" .format(text))

# Считывание из файла
x = []
x.append(X())
index = 0
sum_yes = 0
sum_no = 0
file = open('bayes.txt')
for string in file.read().splitlines():
    if string == '':
        if len(x[index].lines) != 0:
            x.append(X())
            index += 1
    else:
        args = list(string.split('\t'))
        args = [int(a) for a in args]
        x[index].add_line(Line(args[0], args[1]))
        if index == 0:
            sum_yes = sum_yes + args[0]
            sum_no = sum_no + args[1]
# Вызов процедуры подсчета вероятностей
for item in x:
    item.calculate_probabilities(sum_yes, sum_no)
# Вычисление вероятностей "Да" или "Нет"
P_yes = sum_yes / (sum_yes + sum_no)
P_no = sum_no / (sum_yes + sum_no)

# Ввод параметров и проверка их корректности
index1 = -1
while index1 < 0:
    out_green("\nОблачность:")
    answer = input('Солнечно - S / Пасмурно - P / Дождь - D\n')
    if answer.lower() == 's':
        index1 = 0
    elif answer.lower() == 'p':
        index1 = 1
    elif answer.lower() == 'd':
        index1 = 2
    else:
         out_red("Некорректный ввод")

index2 = -1
while index2 < 0:
    out_green("\nТемпература:")
    answer = input('Жарко - J / Тепло - T / Прохладно - P\n')
    if answer.lower() == 'j':
        index2 = 0
    elif answer.lower() == 't':
        index2 = 1
    elif answer.lower() == 'p':
        index2 = 2
    else:
         out_red("Некорректный ввод")

index3 = -1
while index3 < 0:
    out_green("\nВлажность:")
    answer = input('Высокая - V / Нормальная - N\n')
    if answer.lower() == 'v':
        index3 = 0
    elif answer.lower() == 'n':
        index3 = 1
    else:
         out_red("Некорректный ввод")

index4 = -1
while index4 < 0:
    out_green("\nВетер:")
    answer = input('Умеренный - Y / Сильный - S\n')
    if answer.lower() == 'y':
        index4 = 0
    elif answer.lower() == 's':
        index4 = 1
    else:
         out_red("Некорректный ввод")

# Знаменатель формулы наивного Байеса
denominator = x[0].lines[index1].p * x[1].lines[index2].p *x[2].lines[index3].p *x[3].lines[index4].p
# Вычисление вероятности проведения матча
P_bayes_yes = x[0].lines[index1].p_yes * x[1].lines[index2].p_yes * x[2].lines[index3].p_yes * x[3].lines[index4].p_yes * P_yes
P_bayes_yes = P_bayes_yes / denominator
# Вычисление вероятности того, что матч не будет проведен
P_bayes_no = x[0].lines[index1].p_no * x[1].lines[index2].p_no * x[2].lines[index3].p_no * x[3].lines[index4].p_no * P_yes
P_bayes_no = P_bayes_no / denominator

# Вывод нормализованных значений
if P_bayes_yes > P_bayes_no:
    out_green("\nМатч состоится с вероятностью ")
    print(P_bayes_yes / (P_bayes_yes + P_bayes_no))
elif P_bayes_yes < P_bayes_no:
    out_green("\nМатч не состоится, вероятность данного события ")
    print(P_bayes_no / (P_bayes_yes + P_bayes_no))
else:
    out_green("\nВероятности равны")

# for item in x:
#     for i in item.lines:
#         print(i.yes, i.no, i.p_yes, i.p_no, i.p)
#     print('-------')
