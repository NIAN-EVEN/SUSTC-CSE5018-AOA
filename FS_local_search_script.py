from multiprocessing import Pool
from local_search import *
from FlowShop import *


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
        # p = np.loadtxt(file, delimiter=',')
        p = load_data(*file)
        key = {'matrix': p, 'fitness': makespan,
               'record_step': record_step, 'evaluations': evaluation_bound}
        Solution.score_matrix = p.copy()
        Solution.fitness = makespan
        # run each setting 10 times
        for k in range(10):
            for i in range(len(init_method)):
                for f in range(len(funcs)):
                    for m in range(len(moveMethod)):
                        filename = subdir + prefix + "%d-%d-%d-%d.txt" % (e, i, f, m)
                        solution = Solution(init_method[i](p.copy()))
                        task(solution, funcs[f], moveMethod[m], filename, key, False)

def on_server():
    for e, file in enumerate(files):
        # p = np.loadtxt(file, delimiter=',')
        p = load_data(*file)
        key = {'matrix': p, 'fitness': makespan,
               'record_step': record_step, 'evaluations': evaluation_bound}
        Solution.score_matrix = p.copy()
        Solution.fitness = makespan
        process_pool = Pool(16)
        # run each setting 10 times
        for k in range(10):
            for i in range(len(init_method)):
                for f in range(len(funcs)):
                    for m in range(len(moveMethod)):
                        filename = subdir + prefix + "%d-%d-%d-%d.txt" % (e, i, f, m)
                        solution = Solution(init_method[i](p.copy()))
                        process_pool.apply_async(task, args=(solution, funcs[f],
                                                             moveMethod[m], filename, key, True))
                        # task(solution, funcs[f], moveMethod[m], filename, key, True)
        process_pool.close()
        process_pool.join()


# basic setting
# files = ['FS_20j_5m.csv', 'FS_100j_10m.csv']
subdir = "data/FS/"
prefix = "FS-std-"
files = [('tai100_10.txt', 100, 10), ('tai200_20.txt', 200, 20)]
record_step = 50
evaluation_bound = 500000
init_method = [johnson_greedy_order, random_order]
funcs = [adjacent_2_item_change, arbitrary_2_item_change, insertion, inversion]
moveMethod = [True, False]
on_server()
# dbg()
