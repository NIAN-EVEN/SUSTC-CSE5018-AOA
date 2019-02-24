import numpy as np

class City():
    idx = 0
    def __init__(self, loc):
        self.loc = loc
        self.idx = City.idx
        City.idx += 1

class Chromosome():
    def __init__(self, length):
        self.length = length
        self.gene = self.randomInit()

    def randomInit(self):
        return np.random.permutation(self.length).tolist()

    def greedyInit(self, length):
        pass

def func(x):
    return x**2

def distance(c1, c2):
    dsts = 0
    for x1, x2 in zip(c1.loc, c2.loc):
        dsts += (x1 - x2)**2
    return np.sqrt(dsts)

def evaluate(p):
    score = 0
    for i, g in enumerate(p.gene):
        score += adj[i-1, i]
    p.score = score

def select():
    seletedGroup = []
    # 轮盘赌方法
    sum = 0
    for p in pop:
        sum += p.score
    for i in range(selectSize):
        randnum = np.random.rand() * sum
        for i in range()
        seletedGroup.append(pop[int(randnum)])

    return seletedGroup

def crossover(k, p):
    # k-points crossover
    # 安全检查，基因长度是否大于k
    pos = np.random.randint() *
    pass

def mutation(p):
    pass

def multiplication(parents):
    pass

def elimination(offspring, pop):
    pass

def init():
    # 存储城市坐标
    with open("TSP坐标.csv", 'r') as f:
        for line in f.readlines():
            loc = line.split(',')
            for i, l in enumerate(loc):
                loc[i] = float(l)
            cities.append(City(loc))
    # 初始化种群
    for i in range(popSize):
        pop.append(Chromosome(cityNum))

    # 计算邻接矩阵
    for i in range(cityNum):
        for j in range(i, cityNum):
            adj[i, j] = distance(cities[i], cities[j])
            adj[j, i] = adj[i, j]

if __name__ == "__main__":
    ##############################################
    popSize = 10
    generation = 100
    selectSize = 2
    lowerBound = 0
    upperBound = 31 + 1
    dim = 2
    cityNum = 100
    ##############################################
    cities = []
    pop = []
    adj = np.zeros(cityNum, cityNum)
    init(popSize)
    for i in range(generation):
        # evaluate
        for j in range(popSize):
            evaluate(pop[j])
        # select
        parents = select(selectSize, pop)
        # generate offspring
        offspring = multiplication(parents)
        # eliminate
        pop = elimination(offspring, pop)
