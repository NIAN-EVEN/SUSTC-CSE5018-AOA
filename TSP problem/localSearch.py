from TSP import *

def firstMove(order):
    pass

def arbitrary2CityChange(order):
    cityNum = len(order)
    pos = random.sample(list(range(cityNum)), 2)
    tmp = order[pos[0]]
    order[pos[0]] = order[pos[1]]
    order[pos[1]] = tmp
    # TODO: find out why can not disable comment
    # errorDetect(order)

def arbitrary3CityChange(order):
    cityNum = len(order)
    pos = random.sample(list(range(cityNum)), 3)
    tmp = order[pos[0]]
    if random.random() < 0.5:
        order[pos[0]] = order[pos[2]]
        order[pos[2]] = order[pos[1]]
        order[pos[1]] = tmp
    else:
        order[pos[0]] = order[pos[1]]
        order[pos[1]] = order[pos[2]]
        order[pos[2]] = tmp
    # TODO: find out why can not disable comment
    # errorDetect(order)