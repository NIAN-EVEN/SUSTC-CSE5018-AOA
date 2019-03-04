from TSP import *

'''
单独存储一个list记录每一代最好的个体，每一代结束后都进行一遍localsearch
群体的iterative local search, 就是演化算法
'''

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
        score += adj[p.gene[i-1], p.gene[i]]
    p.score = score

def select(num, pop):
    seletedGroup = []
    # 轮盘赌方法
    sum = 0
    for p in pop:
        sum += 1/p.score
    for i in range(num):
        randnum = np.random.rand() * sum
        number = 0
        for p in pop:
            if number <= randnum and number + 1/p.score > randnum:
                seletedGroup.append(p)
                break
            number += 1/p.score

    return seletedGroup

def rankBasedSelect(num, pop):
    selectedGroup = []
    rang = len(pop) * (len(pop) + 1) / 2
    for i in range(num):
        # rand为0-range的随机数
        rand = np.random.rand() * rang
        # 在整个range中j占比∑(1~j-1)-∑(1~j)部分
        # 对rand反向求是哪个数累加而成再加1即实现按照排序选择的功能
        p = int((np.sqrt(8 * rand + 1) - 1) / 2) + 1
        selectedGroup.append(pop[len(pop) - p])

    return selectedGroup

def crossover(p1, p2):
    pos = random.sample(list(range(1, cityNum)), 2)
    pos.sort()
    newGene1 = copy.deepcopy(p1.gene)
    newGene2 = copy.deepcopy(p2.gene)
    exchange1 = [] # gene1有，gene2中没有的
    exchange2 = [] # gene2有，gene1中没有的
    for i in range(pos[0], pos[1]+1):
        newGene1[i] = p2.gene[i]
        newGene2[i] = p1.gene[i]
    for i in range(pos[0], pos[1]+1):
        if newGene1[pos[0]: pos[1]+1].count(newGene2[i]) == 0:
            exchange2.append(newGene2[i])
        if newGene2[pos[0]: pos[1]+1].count(newGene1[i]) == 0:
            exchange1.append(newGene1[i])
    for i in range(0, pos[0]):
        if newGene1[pos[0]: pos[1]+1].count(newGene1[i]) == 1:
            newGene1[i] = exchange2[exchange1.index(newGene1[i])]
        if newGene2[pos[0]: pos[1]+1].count(newGene2[i]) == 1:
            newGene2[i] = exchange1[exchange2.index(newGene2[i])]
    if pos[1]+1 <= p1.length:
        for i in range(pos[1]+1, p1.length):
            if newGene1[pos[0]: pos[1] + 1].count(newGene1[i]) == 1:
                newGene1[i] = exchange2[exchange1.index(newGene1[i])]
            if newGene2[pos[0]: pos[1] + 1].count(newGene2[i]) == 1:
                newGene2[i] = exchange1[exchange2.index(newGene2[i])]
    for k in range(cityNum):
        if newGene1.count(k) > 1 or newGene2.count(k) > 1:
            print("newGene mis")
            exit(-1)

    newChrom1 = Chromosome(p1.length)
    newChrom1.setGene(newGene1)
    evaluate(newChrom1)
    newChrom2 = Chromosome(p2.length)
    newChrom2.setGene(newGene2)
    evaluate(newChrom2)

    return newChrom1, newChrom2

def mutation(p):
    pos = random.sample(list(range(1, cityNum)), 2)
    tmp = p.gene[pos[0]]
    p.gene[pos[0]] = p.gene[pos[1]]
    p.gene[pos[1]] = tmp


def multiplication(parents):
    return crossover(parents[0], parents[1])

def elimination(pop):
    pop.sort(key=lambda x:x.score)
    while len(pop) > popSize:
        pop.pop()

def init():
    # 存储城市坐标
    with open("TSP.csv", 'r') as f:
        print(os.getcwd())
        # for line in f.readlines():
        for i in range(cityNum):
            line = f.readline()
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

    # evaluate
    for i in range(popSize):
        evaluate(pop[i])

def outputInfo(genera):
    print("generation: {0}".format(genera))
    print(pop[0].gene)
    print(pop[0].score)


if __name__ == "__main__":
    ##############################################
    popSize = 1000
    generation = 300000
    selectSize = 2
    lowerBound = 0
    upperBound = 31 + 1
    dim = 2
    cityNum = 100
    muRate = 0.15
    parentSize = 100
    bestScore = 20000
    ##############################################
    cities = []
    pop = []
    adj = np.zeros((cityNum, cityNum))
    init()
    pop.sort(key=lambda x: x.score)
    for i in range(generation):
        # select
        for j in range(parentSize):
            # parents = select(selectSize, pop[0:popSize])
            parents = rankBasedSelect(selectSize, pop[0:popSize])
            # generate offspring
            for offs in multiplication(parents):
                if np.random.rand() < muRate:
                    mutation(offs)
                pop.append(offs)
        # eliminate
        elimination(pop)
        if pop[0].score < bestScore:
            outputInfo(i)
            bestScore = pop[0].score

