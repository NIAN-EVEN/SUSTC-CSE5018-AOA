import copy, random
from greedy import *
from TSP import *
from itertools import combinations

def firstMove(solution, adj):
    # TODO: 写一个通用的firstmove算法
    for pos in combinations(solution.order, 2):
        newOrder = copy.deepcopy(solution.order)
        tmp = newOrder[pos[0]]
        newOrder[pos[0]] = newOrder[pos[1]]
        newOrder[pos[1]] = tmp
        newSolution = Solution(newOrder, adj)
        if newSolution.score < solution.score:
            return newSolution
    return solution

def adjacent2CityChange(order):
    cityNum = len(order)
    pos = [random.sample(list(range(cityNum)), 1)]
    pos.append(pos[0]-1)
    newOrder = copy.deepcopy(order)
    tmp = newOrder[pos[0]]
    newOrder[pos[0]] = newOrder[pos[1]]
    newOrder[pos[1]] = tmp
    errorDetect(newOrder)
    return newOrder

def arbitrary2CityChange(order):
    cityNum = len(order)
    pos = random.sample(list(range(cityNum)), 2)
    newOrder = copy.deepcopy(order)
    tmp = newOrder[pos[0]]
    newOrder[pos[0]] = newOrder[pos[1]]
    newOrder[pos[1]] = tmp
    errorDetect(newOrder)
    return newOrder

def insertion(order):
    cityNum = len(order)
    pos0 = random.sample(list(range(cityNum)), 1)
    pos1 = random.sample(list(range(cityNum-1)), 1)
    # TODO: exam pos1 == pos0
    newOrder = copy.deepcopy(order)
    idx = newOrder.pop(pos0)
    newOrder.insert(pos1, idx)
    errorDetect(newOrder)
    return newOrder

def arbitrary3CityChange(order):
    cityNum = len(order)
    pos = random.sample(list(range(cityNum)), 3)
    newOrder = copy.deepcopy(order)
    tmp = newOrder[pos[0]]
    if random.random() < 0.5:
        newOrder[pos[0]] = newOrder[pos[2]]
        newOrder[pos[2]] = newOrder[pos[1]]
        newOrder[pos[1]] = tmp
    else:
        newOrder[pos[0]] = newOrder[pos[1]]
        newOrder[pos[1]] = newOrder[pos[2]]
        newOrder[pos[2]] = tmp
    errorDetect(newOrder)
    return newOrder

def inversion(order):
    cityNum = len(order)
    pos = random.sample(list(range(cityNum)), 2)
    pos.sort()
    newOrder = copy.deepcopy(order)
    for i in range(pos[0], pos[1]):
        newOrder[i] = order[pos[1]-1-i+pos[0]]
    errorDetect(newOrder)
    return newOrder

def twoTimesInversion(order):
    # TODO 检查两次交叉的路径需要不一样
    newOrder = inversion(order)
    return inversion(newOrder)

def doubleBridge(order):
    cityNum = len(order)
    pos = [np.random.randint(cityNum)]
    for i in range(1, 4):
        newPos = pos[-1]-int(cityNum/4)
        if newPos >= 0:
            pos.append(newPos)
        else:
            pos.append(newPos+cityNum)
    pos.sort()
    pos[-1] -= cityNum
    newOrder = copy.deepcopy(order)
    for i in range(len(pos)):
        if pos[i-1] > pos[i]:
            pos[i] += cityNum
        for j in range(pos[i-1], pos[i]):
            newOrder[j] = order[pos[i] - 1 - j + pos[i-1]]
    return newOrder

def oneLocalSearch(solution, adj):
    bestScore = solution.score
    newSolution = firstMove(solution, adj)
    while newSolution.score < bestScore:
        bestScore = newSolution.score
        newSolution = firstMove(newSolution, adj)
    return newSolution

def iterativeLocalSearch(solution, adj, iterNum):
    pop = [solution]
    newSolution = copy.deepcopy(solution)
    for i in range(iterNum):
        pop.append(oneLocalSearch(newSolution, adj))
        newSolution = Solution(doubleBridge(pop[-1].order), adj)
    return pop


if __name__ == "__main__":
    FILENAME = sys.argv[1]
    CITY_NUM = sys.argv[2]
    GENERATION = sys.argv[3]
    RESULT_FILE = sys.argv[4]

    city = loadCity(FILENAME, CITY_NUM)
    adj = getAdjMatrix(city)

    solution = Solution(greedyTSP(city, adj), adj)

    tofile(RESULT_FILE, GENERATION)
    inversion(solution.order)
    doubleBridge(solution.order)
