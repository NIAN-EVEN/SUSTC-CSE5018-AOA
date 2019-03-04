import numpy as np
import os, sys
import random, copy
from greedy import *
from localSearch import *

class City():
    def __init__(self, idx, loc):
        self.loc = loc
        self.idx = idx

def loadCity(filename, cityNum):
    '''this program need'''
    city = []
    with open(filename, "r") as f:
        for i in range(cityNum):
            line = f.readline()
            location = line.split(',')
            for j, loc in enumerate(location):
                location[j] = float(loc)
            city.append(City(i, np.array(location)))
    return city

def getAdjMatrix(city):
    # 计算邻接矩阵
    cityNum = len(city)
    adj = np.zeros((cityNum, cityNum))
    for i in range(cityNum):
        for j in range(i, cityNum):
            delta = city[i].loc-city[j].loc
            adj[i, j] = np.sqrt(np.dot(delta, delta))
            adj[j, i] = adj[i, j]
    return adj

def evaluateOrder(order, adj):
    f = sys._getframe()
    sys.stderr.write(f.stack)
    score = 0
    for i in range(len(order)):
        score += adj[order[i-1], order[i]]
    return score

def errorDetect(order):
    for o in order:
        if order.count(o) > 1:
            f = sys._getframe()
            for sta in f.stack:
                sys.stderr.write(sta)
            sys.stderr.write("wrong order\n")
            exit(-1)

if __name__ == "__main__":
    CITY_NUM = 10
    FILENAME = "TSP.csv"

    city = loadCity(FILENAME, CITY_NUM)
    adj = getAdjMatrix(city)
    order = greedyTSP(city, adj)
    score = evaluateOrder(order, adj)
    print(order, score)
    arbitrary3CityChange(order)
    score = evaluateOrder(order, adj)
    print(order, score)
