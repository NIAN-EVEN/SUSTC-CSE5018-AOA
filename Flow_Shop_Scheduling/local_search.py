import sys, logging, random
import numpy as np


def swap(order, pos0, pos1):
    tmp = order[pos0]
    order[pos0] = order[pos1]
    order[pos1] = tmp

def adjacent_2_city_change(old_solution, adj, firstMove=False):
    order = old_solution.order
    city_num = len(order)
    bestSoFar = old_solution
    evaluation_num = 0
    for i in range(city_num):
        newOrder = copy.deepcopy(order)
        swap(newOrder, i-1, i)
        new_solution = Solution(newOrder, adj)
        evaluation_num += 1
        if new_solution.score < bestSoFar.score:
            bestSoFar = new_solution
            if firstMove:
                return bestSoFar, evaluation_num
    return bestSoFar, evaluation_num

def arbitrary_2_city_change(old_solution, adj, firstMove=False):
    order = old_solution.order
    bestSoFar = old_solution
    city_num = len(order)
    evaluation_num = 0
    for pos in combinations(list(range(city_num)), 2):
        newOrder = copy.deepcopy(order)
        swap(newOrder, pos[0], pos[1])
        new_solution = Solution(newOrder, adj)
        evaluation_num += 1
        if new_solution.score < bestSoFar.score:
            bestSoFar = new_solution
            if firstMove:
                return bestSoFar, evaluation_num
    return bestSoFar, evaluation_num

def insertion(old_solution, adj, firstMove=False):
    order = old_solution.order
    bestSoFar = old_solution
    city_num = len(order)
    evaluation_num = 0
    for pos0 in range(city_num):
        for pos1 in range(city_num):
            if pos0 == pos1:
                continue
            newOrder = copy.deepcopy(order)
            ct = newOrder.pop(pos0)
            newOrder.insert(pos1, ct)
            new_solution = Solution(newOrder, adj)
            evaluation_num += 1
            if new_solution.score < bestSoFar.score:
                bestSoFar = new_solution
                if firstMove:
                    return bestSoFar, evaluation_num
    return bestSoFar, evaluation_num

def arbitrary_3_city_change(old_solution, adj, firstMove=False):
    order = old_solution.order
    bestSoFar = old_solution
    city_num = len(order)
    evaluation_num = 0
    for combi in combinations(list(range(city_num)), 3):
        for perm in permutations(combi, 3):
            if combi == perm:
                continue
            newOrder = copy.deepcopy(order)
            for pos0, pos1 in zip(combi, perm):
                newOrder[pos0] = order[pos1]
            new_solution = Solution(newOrder, adj)
            evaluation_num += 1
            if new_solution.score < bestSoFar.score:
                bestSoFar = new_solution
                if firstMove:
                    return bestSoFar, evaluation_num
    return bestSoFar, evaluation_num

def inversion(old_solution, adj, firstMove=False):
    order = old_solution.order
    bestSoFar = old_solution
    city_num = len(order)
    evaluation_num = 0
    for pos in combinations(list(range(city_num)), 2):
        pos0 = min(pos)
        pos1 = max(pos)+1
        newOrder = copy.deepcopy(order)
        for i in range(pos0, pos1):
            newOrder[i] = order[pos1 - 1 - (i - pos0)]
        new_solution = Solution(newOrder, adj)
        evaluation_num += 1
        if new_solution.score < bestSoFar.score:
            bestSoFar = new_solution
            if firstMove:
                return bestSoFar, evaluation_num
    return bestSoFar, evaluation_num

def two_times_inversion(old_solution, adj, firstMove=False):
    new_solution1, evaluation_num1 = inversion(old_solution, adj, firstMove)
    new_solution2, evaluation_num2 = inversion(new_solution1, adj, firstMove)
    return new_solution2, evaluation_num2+evaluation_num1

def doubleBridge(order):
    city_num = len(order)
    pos = [np.random.randint(city_num)]
    for i in range(1, 4):
        newPos = pos[-1]-int(city_num/4)
        if newPos >= 0:
            pos.append(newPos)
        else:
            pos.append(newPos+city_num)
    pos.sort()
    pos[-1] -= city_num
    newOrder = copy.deepcopy(order)
    for i in range(len(pos)):
        if pos[i-1] > pos[i]:
            pos[i] += city_num
        for j in range(pos[i-1], pos[i]):
            newOrder[j] = order[pos[i] - 1 - j + pos[i-1]]
    return newOrder

def localSearch(solution, adj, func, firstMove):
    pop = [solution]
    old_solution = copy.deepcopy(solution)
    evaluation_num = 0
    while True:
        new_solution, eval_num = func(old_solution, adj, firstMove)
        evaluation_num += eval_num
        # terminated condition: There is no better solution in neighbours
        if new_solution.score >= old_solution.score:
            pop.append(new_solution)
            break
        if evaluation_num / RECORD_STEP >= len(pop):
            pop.append(new_solution)
        old_solution = new_solution
    return pop, evaluation_num

def iterativeLocalSearch(evaluation_bound, solution, adj, func, firstMove):
    evaluation_num = 0
    iter_pop = [(solution, evaluation_num)]
    new_solution = solution
    while evaluation_num < evaluation_bound:
        pop, eval_num = localSearch(new_solution, adj, func, firstMove)
        evaluation_num += eval_num
        if pop[-1].score < iter_pop[-1][0].score:
            iter_pop.append((pop[-1], evaluation_num))
        new_solution = Solution(doubleBridge(pop[-1].order), adj)
    return iter_pop

def task(eval_bound, solution, adj, func, firstMove, filename):
    print("%s is running..." % (filename))
    start = time.time()
    iter_pop = iterativeLocalSearch(eval_bound, solution, adj, func, firstMove)
    # tofile(filename, iter_pop, start)

def on_server():
    city = loadCity(FILENAME, CITY_NUM)
    adj = getAdjMatrix(city)
    p = Pool()
    for i in range(CITY_NUM):
        greedy_solution = Solution(greedyTSP(city, adj, i), adj)
        random_solution = Solution(randomOrder(CITY_NUM), adj)
        for i in range(len(funcs)):
            # print("at func %s" % func.__name__)
            greedy_file = funcs[i].__name__ + "_greedy"
            random_file = funcs[i].__name__ + "_random"
            for firstMove in (True, False):
                # print("first move is %s" % str(firstMove))
                gre_file = greedy_file + "_firstMove" if firstMove else greedy_file + "_bestMove"
                ran_file = random_file + "_firstMove" if firstMove else random_file + "_bestMove"
                # task(EVAL_BOUND, greedy_solution, adj, func, firstMove, gre_file)
                p.apply_async(task, args=(EVAL_BOUND, greedy_solution, adj, funcs[i], firstMove, gre_file))
                p.apply_async(task, args=(EVAL_BOUND, random_solution, adj, funcs[i], firstMove, ran_file))
    # print("waitting for child process finish")
    p.close()
    p.join()

funcs = [adjacent_2_city_change, arbitrary_2_city_change, arbitrary_3_city_change, insertion,
             inversion, two_times_inversion]
def dbg():
    # objective of this program is to minimize finish time of flow shop

    # random generate a JOB_NUM*MACHINE_NUM table p,
    # p[i][j] is processing time of job i on machine j
    p = np.random.rand(JOB_NUM, MACHINE_NUM) * 100
    # solution is a ordered list consist of index of tasks
    # init a permutation
    # calculate the corresponding finish time
    # put it into localsearch function
    pass

if __name__ == "__main__":
    JOB_NUM = int(sys.argv[1])
    MACHINE_NUM = int(sys.argv[2])


    pass