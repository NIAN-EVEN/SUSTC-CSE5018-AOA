from local_search import *

def hyper_task(solution, funcs, firstMove, filename, kw, save=False):
    Solution.score_matrix = kw['matrix']
    Solution.fitness = kw['fitness']
    print("%s is running..." % (filename))
    start = time.time()
    iter_pop, bestSoFar = iterative_online_choice(kw['evaluations'], solution, funcs, firstMove)
    if save:
        using_time = time.time() - start
        tofile(filename, iter_pop, using_time)
    else:
        print(bestSoFar)

def online_choice(evaluation_bound, score_bound, evaluation_num, solution, funcs, firstMove):
    pop = [solution]
    old_solution = solution
    idx = 0
    while evaluation_num < evaluation_bound and idx < len(funcs):
        new_solution, evaluation = funcs[idx](old_solution, firstMove)
        evaluation_num += evaluation
        new_solution.evaluation_num = evaluation_num
        if new_solution.score >= old_solution.score:
            idx += 1
            continue
        if new_solution.score < score_bound and new_solution.score < pop[-1].score:
            pop.append(new_solution)
            idx = 0
        old_solution = new_solution
    return pop, evaluation_num

def offline_choice():
    pass

def iterative_online_choice(evaluation_bound, solution, funcs, firstMove):
    evaluation_num = 0
    iter_pop = [solution]
    bestSoFar = solution
    old_solution = solution
    while evaluation_num < evaluation_bound:
        pop, evaluation_num = online_choice(evaluation_bound, iter_pop[-1].score, evaluation_num,
                                          old_solution, funcs, firstMove)
        iter_pop.extend(pop[1:])
        if iter_pop[-1].score < bestSoFar.score:
            bestSoFar = iter_pop[-1]
        old_solution = Solution(doubleBridge(pop[-1].order), evaluation=evaluation_num)
    return iter_pop, bestSoFar
