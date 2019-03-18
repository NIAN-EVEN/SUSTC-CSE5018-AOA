import numpy as np
import matplotlib.pyplot as plt
import sys, os, time

class City():
    def __init__(self, idx, loc):
        self.loc = loc
        self.idx = idx

class Solution():
    def __init__(self, order, adj):
        self.order = order
        self.score = evaluateOrder(order, adj)

    def __str__(self):
        return str(self.order) + "\n" + str(self.score)

    def toGraph(self, cities, directory, name, show=False):
        plt.figure()
        X = np.zeros(len(cities)+1)
        Y = np.zeros(len(cities)+1)
        for i, city in enumerate(cities):
            X[i] = city.loc[0]
            Y[i] = city.loc[1]
        X[-1] = cities[0].loc[0]
        Y[-1] = cities[0].loc[1]
        plt.scatter(X, Y)
        plt.plot(X, Y)
        plt.savefig(directory + name)
        if show:
            plt.show()


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
    score = 0
    for i in range(len(order)):
        score += adj[order[i-1], order[i]]
    return score

def errorDetect(order):
    for o in range(len(order)):
        if order.count(o) > 1:
            print("error")
            exit(-1)

def tofile(rstfile, pop, start, eval_num):
    with open(rstfile, 'w') as f:
        f.write("using time: %f sec " % (time.time() - start))
        f.write("evaluation num = %d\n" % eval_num)
        for i, p in enumerate(pop):
            f.write(str(i)+" | "+str(p.order)+" | "+str(p.score)+"\n")
        f.write("\n")
