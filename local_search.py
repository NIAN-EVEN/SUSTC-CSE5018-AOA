from copy import deepcopy
from itertools import combinations, permutations
from numpy.random import randint
import time
# import numpy as np

class Solution:
    score_matrix = None
    fitness = None
    def __init__(self, order, score=None, evaluation=0):
        self.order = order
        if score == None:
            self.score = Solution.fitness(order, Solution.score_matrix)
        else:
            self.score = score
        self.evaluation_num = evaluation

    def __str__(self):
        return 'evaluation=%d, score=%d, order=%s' % (self.evaluation_num, self.score, str(self.order))

def tofile(rstfile, pop, using_time):
    with open(rstfile, 'a') as f:
        f.write("using time = %f sec, evaluation num = %d\n" %
                (using_time, pop[-1].evaluation_num))
        for p in pop:
            f.write("%s\n" % str(p))
        f.write("\n")

def task(solution, func, firstMove, filename, kw, save=False):
    Solution.score_matrix = kw['matrix']
    Solution.fitness = kw['fitness']
    print("%s is running..." % (filename))
    start = time.time()
    iter_pop, bestSoFar = iterativeLocalSearch(kw['evaluations'], solution, func, firstMove)
    if save:
        using_time = time.time() - start
        tofile(filename, iter_pop, using_time)
    else:
        print(bestSoFar)

def swap(order, pos0, pos1):
    tmp = order[pos0]
    order[pos0] = order[pos1]
    order[pos1] = tmp

def adjacent_2_item_change(old_solution, firstMove=True):
    order = old_solution.order
    item_num = len(order)
    bestSoFar = old_solution
    evaluation_num = 0
    for i in range(item_num):
        new_order = order.copy()
        swap(new_order, i-1, i)
        new_solution = Solution(new_order)
        evaluation_num += 1
        if new_solution.score < bestSoFar.score:
            bestSoFar = new_solution
            if firstMove:
                return bestSoFar, evaluation_num
    return bestSoFar, evaluation_num

def arbitrary_2_item_change(old_solution, firstMove=True):
    order = old_solution.order
    bestSoFar = old_solution
    item_num = len(order)
    evaluation_num = 0
    for pos in combinations(list(range(item_num)), 2):
        new_order = order.copy()
        swap(new_order, pos[0], pos[1])
        new_solution = Solution(new_order)
        evaluation_num += 1
        if new_solution.score < bestSoFar.score:
            bestSoFar = new_solution
            if firstMove:
                return bestSoFar, evaluation_num
    return bestSoFar, evaluation_num

def insertion(old_solution, firstMove=True):
    order = old_solution.order
    bestSoFar = old_solution
    item_num = len(order)
    evaluation_num = 0
    for pos0 in range(item_num):
        for pos1 in range(item_num):
            if pos0 == pos1:
                continue
            new_order = order.copy()
            ct = new_order.pop(pos0)
            new_order.insert(pos1, ct)
            new_solution = Solution(new_order)
            evaluation_num += 1
            if new_solution.score < bestSoFar.score:
                bestSoFar = new_solution
                if firstMove:
                    return bestSoFar, evaluation_num
    return bestSoFar, evaluation_num

def arbitrary_3_item_change(old_solution, firstMove=True):
    order = old_solution.order
    bestSoFar = old_solution
    item_num = len(order)
    evaluation_num = 0
    for combi in combinations(list(range(item_num)), 3):
        for perm in permutations(combi, 3):
            if combi == perm:
                continue
            new_order = order.copy()
            for pos0, pos1 in zip(combi, perm):
                new_order[pos0] = order[pos1]
            new_solution = Solution(new_order)
            evaluation_num += 1
            if new_solution.score < bestSoFar.score:
                bestSoFar = new_solution
                if firstMove:
                    return bestSoFar, evaluation_num
    return bestSoFar, evaluation_num

def inversion(old_solution, firstMove=True):
    order = old_solution.order
    bestSoFar = old_solution
    item_num = len(order)
    evaluation_num = 0
    for pos in combinations(list(range(item_num)), 2):
        pos0 = min(pos)
        pos1 = max(pos)+1
        new_order = order.copy()
        for i in range(pos0, pos1):
            new_order[i] = order[pos1 - 1 - (i - pos0)]
        new_solution = Solution(new_order)
        evaluation_num += 1
        if new_solution.score < bestSoFar.score:
            bestSoFar = new_solution
            if firstMove:
                return bestSoFar, evaluation_num
    return bestSoFar, evaluation_num

def two_times_inversion(old_solution, firstMove=True):
    new_solution1, evaluation_num1 = inversion(old_solution, firstMove)
    new_solution2, evaluation_num2 = inversion(new_solution1, firstMove)
    return new_solution2, evaluation_num2+evaluation_num1

def doubleBridge(order):
    item_num = len(order)
    pos = [randint(item_num)]
    for i in range(1, 4):
        newPos = pos[-1]-int(item_num/4)
        if newPos >= 0:
            pos.append(newPos)
        else:
            pos.append(newPos+item_num)
    pos.sort()
    pos[-1] -= item_num
    new_order = order.copy()
    for i in range(len(pos)):
        if pos[i-1] > pos[i]:
            pos[i] += item_num
        for j in range(pos[i-1], pos[i]):
            new_order[j] = order[pos[i] - 1 - j + pos[i-1]]
    return new_order

def localSearch(evaluation_bound, score_bound, evaluation_num, solution, func, firstMove):
    pop = [solution]
    old_solution = solution
    while evaluation_num < evaluation_bound:
        new_solution, eval_num = func(old_solution, firstMove)
        evaluation_num += eval_num
        new_solution.evaluation_num = evaluation_num
        # terminated condition: There is no better solution in neighbours
        if new_solution.score >= old_solution.score:
            break
        if new_solution.score < score_bound and new_solution.score < pop[-1].score:
            pop.append(new_solution)
        old_solution = new_solution
    return pop, evaluation_num

def iterativeLocalSearch(evaluation_bound, solution, func, firstMove):
    evaluation_num = 0
    iter_pop = [solution]
    bestSoFar = solution
    old_solution = solution
    while evaluation_num < evaluation_bound:
        pop, evaluation_num = localSearch(evaluation_bound, iter_pop[-1].score, evaluation_num,
                                          old_solution, func, firstMove)
        iter_pop.extend(pop[1:])
        if iter_pop[-1].score < bestSoFar.score:
            bestSoFar = iter_pop[-1]
        old_solution = Solution(doubleBridge(pop[-1].order), evaluation=evaluation_num)
    return iter_pop, bestSoFar
