import numpy as np
import os

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

    def setGene(self, gene):
        self.gene = gene

def distance(c1, c2):
    dsts = 0
    for x1, x2 in zip(c1.loc, c2.loc):
        dsts += (x1 - x2)**2
    return np.sqrt(dsts)

def evaluate(p):
    score = 0
    for i in range(p.length):
        c1 = cities[p.gene[i-1]]
        c2 = cities[p.gene[i]]
        score += distance(c1, c2)
    p.score = score

def select(num, pop):
    seletedGroup = []
    # 轮盘赌方法
    sum = 0
    for p in pop:
        sum += 1/p.score
    for i in range(selectSize):
        randnum = np.random.rand() * sum
        number = 0
        for p in pop:
            if number <= randnum and number + p.score > randnum:
                seletedGroup.append(p)
                break
            number += 1/p.score

    return seletedGroup

def crossover(p1, p2, k = 2):
    # k-points crossover
    # 安全检查，基因长度是否大于k
    if k > 100:
        print("k is {0}, gene length is {1}".format(k, p1.length))
        exit(-1)
    pos = [0]
    for i in range(k):
        if pos[i] + 1 == p1.length:
            break
        temp = np.random.randint(pos[i]+1, p1.length) # here there may be a lot of p1.gene in p
        pos.append(temp)
    # 交叉奇数段
    newGene1 = []
    newGene2 = []
    for i in range(p1.length):
        if i in pos and i % 2 == 1:
            newGene1.append(p2.gene[i])
            newGene2.append(p1.gene[i])
            for j in range(i):
                if newGene1[j] == newGene1[-1]:
                    newGene1[j] = p1.gene[i]
                if newGene2[j] == newGene2[-1]:
                    newGene2[j] = p2.gene[i]
        else:
            newGene1.append(p1.gene[i])
            newGene2.append(p2.gene[i])

    newChrom1 = Chromosome(p1.length)
    newChrom1.setGene(newGene1)
    evaluate(newChrom1)
    newChrom2 = Chromosome(p2.length)
    newChrom2.setGene(newGene2)
    evaluate(newChrom2)

    return newChrom1, newChrom2

def mutation(p):
    pos1 = np.random.randint(0, p.length)
    if pos1+1 == p.length:
        pos2 = pos1
    else:
        pos2 = np.random.randint(pos1+1, p.length)
    tmp = p.gene[pos1]
    p.gene[pos1] = p.gene[pos2]
    p.gene[pos2] = tmp

def multiplication(parents):
    return crossover(parents[0], parents[1])

def elimination(pop):
    pop.sort(key=lambda x:x.score)
    while len(pop) > popSize:
        pop.pop()

def init():
    # 存储城市坐标
    with open("TSP.csv", 'r', encoding="cp936") as f:
        print(os.getcwd())
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

def outputInfo(genera):
    print("generation: {0}".format(genera))
    print(pop[0].gene)
    print(pop[0].score)

if __name__ == "__main__":
    ##############################################
    popSize = 50
    generation = 1000
    selectSize = 2
    lowerBound = 0
    upperBound = 31 + 1
    dim = 2
    cityNum = 100
    muRate = 0.02
    ##############################################
    cities = []
    pop = []
    adj = np.zeros((cityNum, cityNum))
    init()
    # evaluate
    for i in range(popSize):
        evaluate(pop[i])
    for i in range(generation):
        # select
        for j in range(selectSize):
            parents = select(2, pop[0:popSize])
            # generate offspring
            for offs in multiplication(parents):
                if np.random.rand() < muRate:
                    mutation(offs)
                pop.append(offs)
        # eliminate
        elimination(pop)
        outputInfo(i)

