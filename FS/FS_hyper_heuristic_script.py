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
    for e, file in enumerate(files):
        p = np.loadtxt(file, delimiter=',')
        key = {'matrix': p, 'fitness': makespan,
               'record_step': 50, 'evaluations': 500000}
        Solution.score_matrix = p.copy()
        Solution.fitness = makespan
        for k in range(10):
            for i in range(len(init_method)):
                for m in range(1):
                    filename = sub_dir + prefix + "%d-%d-%d.txt" % (e, i, m)
                    solution = Solution(init_method[i](p.copy()))
                    hyper_task(solution, funcs, moveMethod[m], filename, key, save=True)

def on_server():
    for e, file in enumerate(files):
        p = np.loadtxt(file, delimiter=',')
        key = {'matrix': p, 'fitness': makespan,
               'record_step': 50, 'evaluations': 500000}
        Solution.score_matrix = p.copy()
        Solution.fitness = makespan
        process_pool = Pool(4)
        for k in range(10):
            for i in range(len(init_method)):
                for m in range(1):
                    filename = sub_dir + prefix + "%d-%d-%d.txt" % (e, i, m)
                    print(filename)
                    solution = Solution(init_method[i](p.copy()))
                    process_pool.apply_async(hyper_task, args=(solution, funcs,
                                                               moveMethod[m], filename, key, True))
        process_pool.close()
        process_pool.join()


# basic setting
sub_dir = 'data/FS/'
prefix = 'hyper_heuristic_simple_order-'
files = ['FS_20j_5m.csv', 'FS_100j_10m.csv']
init_method = [johnson_greedy_order, random_order]
funcs = [adjacent_2_item_change, arbitrary_2_item_change, inversion, insertion]
moveMethod = [True, False]
# different experimental settings
# dbg()
on_server()
import numpy as np

np.linspace(-100, 100, 5)
