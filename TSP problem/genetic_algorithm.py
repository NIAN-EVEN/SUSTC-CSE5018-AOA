import numpy as np
import random, copy, time, sys
from itertools import combinations
from TSP import *
from localSearch import *
from greedy import *
'''
单独存储一个list记录每一代最好的个体，每一代结束后都进行一遍localsearch
群体的iterative local search, 就是演化算法
'''

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

def crossover(order1, order2, crossSize):
    cityNum = len(order1)
    # 因为是排序问题，所以一定是成段基因含有有效信息，离散基因无效
    pos = [np.random.randint(cityNum)]
    pos.insert(0, int(pos[0]-crossSize))

    newOrder1 = copy.deepcopy(order1)
    newOrder2 = copy.deepcopy(order2)

    if pos[0] < 0:
        for i in range(cityNum):
            newOrder1[i] = order1[i+pos[0]]
            newOrder2[i] = order2[i+pos[0]]
        pos[1] -= pos[0]
        pos[0] = 0

    exchange1 = [] # gene1有，gene2中没有的
    exchange2 = [] # gene2有，gene1中没有的
    # 交叉
    for i in range(pos[0], pos[1]):
        tmp = newOrder1[i]
        newOrder1[i] = newOrder2[i]
        newOrder2[i] = tmp
    # 计算缺省对应关系
    for i in range(pos[0], pos[1]):
        if pos[0] < 0:
            print(newOrder1[pos[0]: pos[1]])
        if newOrder1[pos[0]: pos[1]].count(newOrder2[i]) == 0:
            exchange2.append(newOrder2[i])
        if newOrder2[pos[0]: pos[1]].count(newOrder1[i]) == 0:
            exchange1.append(newOrder1[i])
    for i in range(0, pos[0]):
        if newOrder1[pos[0]: pos[1]].count(newOrder1[i]) == 1:
            newOrder1[i] = exchange2[exchange1.index(newOrder1[i])]
        if newOrder2[pos[0]: pos[1]].count(newOrder2[i]) == 1:
            newOrder2[i] = exchange1[exchange2.index(newOrder2[i])]
    for i in range(pos[1], cityNum):
        if newOrder1[pos[0]: pos[1]].count(newOrder1[i]) == 1:
            newOrder1[i] = exchange2[exchange1.index(newOrder1[i])]
        if newOrder2[pos[0]: pos[1]].count(newOrder2[i]) == 1:
            newOrder2[i] = exchange1[exchange2.index(newOrder2[i])]


    errorDetect(newOrder1)
    errorDetect(newOrder2)

    return newOrder1, newOrder2

def reproduction(parents, adj, crossSize):
    newOrder1, newOrder2 = crossover(parents[0].order, parents[1].order, crossSize)
    return iterativeLocalSearch(Solution(newOrder1, adj), adj), iterativeLocalSearch(Solution(newOrder2, adj), adj)

def mutation(solution, adj):
    newOrder = doubleBridge(solution.order)
    return iterativeLocalSearch(Solution(newOrder, adj), adj)

def init(filename, cityNum, popSize):
    city = loadCity(filename, cityNum)
    adj = getAdjMatrix(city)
    # TODO: greedy local init
    # order = greedyTSP(city, adj)
    # randomly init
    pop = []
    for i in range(popSize):
        order = np.random.permutation(cityNum).tolist()
        solution = iterativeLocalSearch(Solution(order, adj), adj)
        pop.append(solution)
    pop.sort(key=lambda x:x.score)

    return pop, adj

def stop(crossSize, time):
    if crossSize == 0 or time > TIME_LIMIT:
        return False
    else:
        return True

if __name__ == "__main__":
    ##############################################
    FILENAME = "TSP.csv"
    POPSIZE =  10
    GENERATION =  300000
    CITY_NUM =  10
    TIME_LIMIT =  12*60*60
    MAX_STAY_NUM =  50
    RESULT_FILE =  "GAresult.csv"
    ##############################################
    pop, adj = init(FILENAME, CITY_NUM, POPSIZE)
    start = time.time()
    crossSize = CITY_NUM/2
    generaSolution = [pop[0]]
    # stayRocord++ when position i is not better than before
    stayRecord = [0 for i in range(POPSIZE)]
    scoreRecord = [x.score for x in pop]
    generation = 1
    bestScore = 8000
    bestGeneration = 1
    while stop(crossSize, start-time.time()):
        # 平均距离越短的段我们认为是较优段，遗传的时候应尽量保留较优段
        # select
        for parents in combinations(pop, 2):
            for off in reproduction(parents, adj, crossSize):
                pop.append(off)
        pop.sort(key=lambda x: x.score)
        del pop[POPSIZE+1, len(pop)+1]
        for i in range(POPSIZE):
            if scoreRecord[i] > pop[i].score:
                scoreRecord[i] = pop[i].score
            else:
                stayRecord[i] += 1
            if stayRecord[i] >= MAX_STAY_NUM:
                pop[i] = mutation(pop[i], adj)
        pop.sort(key=lambda x: x.score)
        generation += 1
        generaSolution.append(pop[0])
        if generation-bestGeneration == 100 and pop[0].score == bestScore:
            crossSize -= 1
        if pop[0].score < bestScore:
            bestScore = pop[0].score
            bestGeneration = generation
            print("generation: ", generation)
            print(pop[0])
    tofile(RESULT_FILE, generaSolution)