import numpy as np
import sys, os, re
import matplotlib.pyplot as plt

class City():
    def __init__(self, idx, loc):
        self.loc = loc
        self.idx = idx

def toGraph(solution, cities, directory, name, show=False):
    plt.figure()
    X = np.zeros(len(cities)+1)
    Y = np.zeros(len(cities)+1)
    for i, od in enumerate(solution.order):
        X[i] = cities[od].loc[0]
        Y[i] = cities[od].loc[1]
    X[-1] = cities[solution.order[0]].loc[0]
    Y[-1] = cities[solution.order[0]].loc[1]
    plt.scatter(X, Y)
    plt.plot(X, Y)
    plt.title("%s (tour length=%d)" % (name, solution.score))
    plt.savefig(directory + '\\' + name)
    if show:
        plt.show()


##################### basic operation ##########################################
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

def tour_length(order, adj):
    score = 0
    for i in range(len(order)):
        score += adj[order[i-1], order[i]]
    return score

def errorDetect(order):
    for o in range(len(order)):
        if order.count(o) > 1:
            print("error")
            exit(-1)

######################## initialization method #############################
def greedyTSP(city, adj, startFrom = 0):
    '''
    return a greedy TSP order start from the parameter
    :param city:
    :param adj:
    :param startFrom:
    :return: a list stores TSP order
    '''
    cityNum = len(city)
    order = [startFrom]
    for i in range(cityNum-1):
        options = adj[order[-1]]
        nextDistance = sys.float_info.max
        for idx, value in enumerate(options):
            if idx != order[-1] and order.count(idx)==0 and value < nextDistance:
                nextCity = idx
                nextDistance = value
        order.append(nextCity)
    # errorDetect(order)
    return order

def greedyTSP_full_order(city, adj):
    '''
    get all possible order of greedy TSP, using start from every city
    :param city:
    :param adj:
    :return: a list contains all possible order
    '''
    cityNum = len(city)
    orders = []
    for i in range(cityNum):
        orders.append(greedyTSP(city, adj, startFrom=i))
    return orders

def randomTSP(city, adj, seed = 0):
    np.random.seed(seed)
    cityNum = len(city)
    order = np.random.permutation(list(range(cityNum)))
    return order.tolist()