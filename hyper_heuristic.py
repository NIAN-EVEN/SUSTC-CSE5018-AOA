from local_search import *
from FlowShop import *

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

if __name__ == "__main__":
    # use flowshop as example
    filename = 'tai100_10.txt'
    job_num = 100
    machine_num = 10
    init_method = johnson_greedy_order
    firstMove = True
    evaluation_bound = 10000
    funcs = funcs_del_adj = [adjacent_2_item_change,
                             arbitrary_2_item_change_del_adj,
                             inversion_del_adj, insertion_del_adj]

    # initialization
    p = load_data(filename, job_num, machine_num)
    Solution.fitness = makespan
    Solution.score_matrix = p.copy()
    solution = Solution(init_method(p.copy()))

    # start running
    start = time.time()
    iter_pop, bestSoFar = iterative_online_choice(evaluation_bound, solution, funcs, firstMove)

    # print result
    using_time = time.time() - start
    print(bestSoFar)
