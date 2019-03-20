import copy, time, logging
from greedy import *
from TSP import *
from itertools import combinations, permutations
from multiprocessing import Process, Pool


def swap(order, pos0, pos1):
    tmp = order[pos0]
    order[pos0] = order[pos1]
    order[pos1] = tmp

def adjacent_2_city_change(oldSolution, adj, firstMove=False):
    order = oldSolution.order
    cityNum = len(order)
    bestSoFar = oldSolution
    evaluation_num = 0
    for i in range(cityNum):
        newOrder = copy.deepcopy(order)
        swap(newOrder, i-1, i)
        newSolution = Solution(newOrder, adj)
        evaluation_num += 1
        if newSolution.score < bestSoFar.score:
            bestSoFar = newSolution
            if firstMove:
                return bestSoFar, evaluation_num
    return bestSoFar, evaluation_num

def arbitrary_2_city_change(oldSolution, adj, firstMove=False):
    order = oldSolution.order
    bestSoFar = oldSolution
    cityNum = len(order)
    evaluation_num = 0
    for pos in combinations(list(range(cityNum)), 2):
        newOrder = copy.deepcopy(order)
        swap(newOrder, pos[0], pos[1])
        newSolution = Solution(newOrder, adj)
        evaluation_num += 1
        if newSolution.score < bestSoFar.score:
            bestSoFar = newSolution
            if firstMove:
                return bestSoFar, evaluation_num
    return bestSoFar, evaluation_num

def insertion(oldSolution, adj, firstMove=False):
    order = oldSolution.order
    bestSoFar = oldSolution
    cityNum = len(order)
    evaluation_num = 0
    for pos0 in range(cityNum):
        for pos1 in range(cityNum):
            if pos0 == pos1:
                continue
            newOrder = copy.deepcopy(order)
            ct = newOrder.pop(pos0)
            newOrder.insert(pos1, ct)
            newSolution = Solution(newOrder, adj)
            evaluation_num += 1
            if newSolution.score < bestSoFar.score:
                bestSoFar = newSolution
                if firstMove:
                    return bestSoFar, evaluation_num
    return bestSoFar, evaluation_num

def arbitrary_3_city_change(oldSolution, adj, firstMove=False):
    order = oldSolution.order
    bestSoFar = oldSolution
    cityNum = len(order)
    evaluation_num = 0
    for combi in combinations(list(range(cityNum)), 3):
        for perm in permutations(combi, 3):
            if combi == perm:
                continue
            newOrder = copy.deepcopy(order)
            for pos0, pos1 in zip(combi, perm):
                newOrder[pos0] = order[pos1]
            newSolution = Solution(newOrder, adj)
            evaluation_num += 1
            if newSolution.score < bestSoFar.score:
                bestSoFar = newSolution
                if firstMove:
                    return bestSoFar, evaluation_num
    return bestSoFar, evaluation_num

def inversion(oldSolution, adj, firstMove=False):
    order = oldSolution.order
    bestSoFar = oldSolution
    cityNum = len(order)
    evaluation_num = 0
    for pos in combinations(list(range(cityNum)), 2):
        pos0 = min(pos)
        pos1 = max(pos)+1
        newOrder = copy.deepcopy(order)
        for i in range(pos0, pos1):
            newOrder[i] = order[pos1 - 1 - (i - pos0)]
        newSolution = Solution(newOrder, adj)
        evaluation_num += 1
        if newSolution.score < bestSoFar.score:
            bestSoFar = newSolution
            if firstMove:
                return bestSoFar, evaluation_num
    return bestSoFar, evaluation_num

def two_times_inversion(oldSolution, adj, firstMove=False):
    newSolution1, evaluation_num1 = inversion(oldSolution, adj, firstMove)
    newSolution2, evaluation_num2 = inversion(newSolution1, adj, firstMove)
    return newSolution2, evaluation_num2+evaluation_num1

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

def iterativeLocalSearch(solution, adj, func, firstMove):
    pop = [solution]
    oldSolution = copy.deepcopy(solution)
    evaluation_num = 0
    while True:
        newSolution, eval_num = func(oldSolution, adj, firstMove)
        evaluation_num += eval_num
        # terminated condition: There is no better solution in neighbours
        if newSolution.score >= oldSolution.score:
            pop.append(newSolution)
            break
        if evaluation_num % 100 == 0:
            pop.append(newSolution)
        oldSolution = newSolution
    return pop, evaluation_num

def iterate_iterativeLocalSearch(evaluation_bound, solution, adj, func, firstMove):
    evaluation_num = 0
    iter_pop = [(solution, evaluation_num)]
    newSolution = solution
    while evaluation_num < evaluation_bound:
        pop, eval_num = iterativeLocalSearch(newSolution, adj, func, firstMove)
        evaluation_num += eval_num
        if pop[-1].score < iter_pop[-1][0].score:
            iter_pop.append((pop[-1], evaluation_num))
        newSolution = Solution(doubleBridge(pop[-1].order), adj)
    return iter_pop

def task(eval_bound, solution, adj, func, firstMove, filename):
    print("%s is running..." % (filename))
    start = time.time()
    iter_pop = iterate_iterativeLocalSearch(eval_bound, solution, adj, func, firstMove)
    tofile(filename, iter_pop, start)

funcs = [adjacent_2_city_change, arbitrary_2_city_change, arbitrary_3_city_change, insertion,
             inversion, two_times_inversion]
# funcs = [adjacent_2_city_change, arbitrary_2_city_change, arbitrary_3_city_change]
# funcs = [insertion, inversion, two_times_inversion]


if __name__ == "__main__":
    FILENAME = sys.argv[1]
    CITY_NUM = int(sys.argv[2])
    EVAL_BOUND = int(sys.argv[3])

    city = loadCity(FILENAME, CITY_NUM)
    adj = getAdjMatrix(city)
    p = Pool()
    for i in range(CITY_NUM):
        greedy_solution = Solution(greedyTSP(city, adj, i), adj)
        random_solution = Solution(randomOrder(CITY_NUM), adj)
        for func in funcs:
            # print("at func %s" % func.__name__)
            greedy_file = func.__name__ + "_greedy"
            random_file = func.__name__ + "_random"
            for firstMove in (True, False):
                # print("first move is %s" % str(firstMove))
                gre_file = greedy_file + "_firstMove" if firstMove else greedy_file + "_bestMove"
                ran_file = random_file + "_firstMove" if firstMove else random_file + "_bestMove"
                # task(EVAL_BOUND, greedy_solution, adj, func, firstMove, gre_file)
                p.apply_async(task, args=(EVAL_BOUND, greedy_solution, adj, func, firstMove, gre_file))
                p.apply_async(task, args=(EVAL_BOUND, random_solution, adj, func, firstMove, ran_file))
    # print("waitting for child process finish")
    p.close()
    p.join()
