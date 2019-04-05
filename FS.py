from numpy import array, zeros
from random import shuffle
from sys import float_info
from local_search import *
from multiprocessing import Pool
import numpy as np

def makespan(job_order, p):
    machine_num = p.shape[1]
    machine_time = zeros(machine_num)
    for jdx in job_order:
        for m, cur_time in enumerate(machine_time):
            if m == 0:
                pre_time = cur_time
            else:
                pre_time = machine_time[m-1]
            machine_time[m] = max(cur_time, pre_time) + p[jdx][m]
    return machine_time[-1]

def johnson_greedy_order(p):
    '''
    @:param p 为 job i 在 machine j 上的处理时间
    use johnson method,
    just consider the first and the last machine
    '''
    job_num = p.shape[0]
    process_order = zeros(job_num, dtype=int)
    machine0 = p[:, 0]
    machine1 = p[:, -1]
    front = 0
    tail = job_num - 1
    while front <= tail:
        min0 = machine0.min()
        min1 = machine1.min()
        if min0 < min1:
            pos = machine0.argmin()
            process_order[front] = pos
            front += 1
        else:
            pos = machine1.argmin()
            process_order[tail] = pos
            tail -= 1
        machine0[pos] = float_info.max
        machine1[pos] = float_info.max

    return process_order.tolist()

def random_order(p):
    task_num = p.shape[0]
    order = list(range(task_num))
    shuffle(order)
    return order

def check_correctness(p, order):
    job_num = p.shape[0]
    for job in range(job_num):
        if order.count(job) > 1:
            print('wrong job order')

def testMakespan():
    p = array([[20, 70], [40, 50], [60, 30], [80, 10], [100, 40], [120, 80], [140, 70]], dtype=float)
    order = johnson_greedy_order(p.copy())
    time = makespan(order, p)
    print('time = %d' % time)

def testGreedy():
    p = array([[20, 70], [40, 50], [60, 30], [80, 10], [100, 40], [120, 80], [140, 70]], dtype=float)
    order = johnson_greedy_order(p.copy())
    print(order)

def on_server():
    P = Pool(2)
    for i, init in enumerate(init_method):
        for f, func in enumerate(funcs):
            for m, firstMove in enumerate(moveMethod):
                solution = Solution(init(p.copy()))
                filename = "data/FS/FS-%d-%d-%d-%d" % (e, i, f, m)
                P.apply_async(task, args=(solution, func, firstMove,
                                          filename, key, True))

files = ['FS_20j_5m.csv', 'FS_100j_10m.csv']
init_method = [johnson_greedy_order, random_order]
funcs = [adjacent_2_item_change, arbitrary_2_item_change, arbitrary_3_item_change,
         insertion, inversion, two_times_inversion]
moveMethod = [True, False]

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
    for i, init in enumerate(init_method):
        for f, func in enumerate(funcs):
            for m, firstMove in enumerate(moveMethod):
                solution = Solution(init(p.copy()))
                filename = "data/FS/FS-%d-%d-%d-%d" % (e, i, f, m)
                task(solution, func, firstMove, filename, key)

if __name__ == "__main__":
    for e, file in enumerate(files):
        p = np.loadtxt(file, delimiter=',')
        key = {'matrix': p, 'fitness': makespan,
               'evaluations': 1000, 'record_step': 50}
        Solution.score_matrix = p.copy()
        Solution.fitness = makespan
        on_server()

# 高斯过程
# 期望改进策略
# EGO algorithm 高斯全局优化算法
# ParEGO algorithm 多目标转换单目标
# MOEAD-EGO

# multi-objective ##################
# 1.
# NAGA-II nondominate front
# crowd-distance algorithm

# 2.
# 假设均匀权值产生均匀解
# 函数的平，凹，凸分布分别对应不同的均匀密度

# 3.
# 多目标转单目标？？？？？？？

# 4.
# 问题规模
# CSO: competitive swarm optimizer

# EDA estimation distribution algorithm