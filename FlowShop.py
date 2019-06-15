from numpy import array, zeros
from random import shuffle
from sys import float_info
import numpy as np
import os, re


########################### basic operation ############################
def load_data(filename, job_num, machine_num):
    p = np.zeros(shape=(machine_num, job_num))
    with open(filename, 'r') as f:
        for i in range(machine_num):
            n_machine = f.readline().strip('\n').strip()
            time_on_n_machine = re.split(r'\s+', n_machine)
            for j, t in enumerate(time_on_n_machine):
                p[i, j] = int(t)
    return p.T

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

if __name__ == "__main__":
    testMakespan()
    testGreedy()
