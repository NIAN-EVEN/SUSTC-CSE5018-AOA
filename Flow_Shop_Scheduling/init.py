import numpy as np
from random import shuffle

def greedy_order(task_num, p):
    '''
    use johnson method,
    just consider the first and the last machine
    '''
    machine0 = p[:, 0]
    machine1 = p[:, -1]

    pass

def random_order(task_num):
    order = list(range(task_num))
    shuffle(order)
    return order