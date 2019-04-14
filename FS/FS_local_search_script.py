from FS.FS import *

def dbg():
    '''
    objective of this program is to minimize finish time of flow shop
    p[i][j] is processing time of job i on machine j
    solution is a ordered list consist of index of tasks
    init a permutation
    calculate the corresponding finish time
    put it into localsearch function
    :return:
    '''
    for i in range(len(init_method)):
        for f in range(len(funcs)):
            for m in range(len(moveMethod)):
                filename = "data/FS/FS-%d-%d-%d-%d.txt" % (e, i, f, m)
                solution = Solution(init_method[i](p.copy()))
                time = solution.score
                new_solution, eval_num = funcs[f](solution, moveMethod[m])
                print("%s: %-4d, %-6d to %-8d" % (filename, eval_num, time, new_solution.score))

def on_server():
    # multiprocess
    process_pool = Pool(4)
    # run each setting 10 times
    for k in range(10):
        for i in range(len(init_method)):
            for f in range(len(funcs)):
                for m in range(len(moveMethod)):
                    filename = "data/FS/FS-%d-%d-%d-%d.txt" % (e, i, f, m)
                    solution = Solution(init_method[i](p.copy()))
                    # process_pool.apply_async(online_choice, args=(solution, funcs,
                    #                                      moveMethod[m], filename, key, True))
                    iterativeLocalSearch(solution, funcs[f], moveMethod[m], filename, key, True)
    process_pool.close()
    process_pool.join()


# basic setting
files = ['FS_20j_5m.csv', 'FS_100j_10m.csv']
init_method = [johnson_greedy_order, random_order]
funcs = [adjacent_2_item_change, arbitrary_2_item_change, arbitrary_3_item_change,
         insertion, inversion, two_times_inversion]
moveMethod = [True, False]
# different experimental settings
for e, file in enumerate(files):
    p = np.loadtxt(file, delimiter=',')
    key = {'matrix': p, 'fitness': makespan,
           'record_step': 50, 'evaluations': 500000}
    Solution.score_matrix = p.copy()
    Solution.fitness = makespan
    on_server()
