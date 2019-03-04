from greedy import *
from localSearch import *
from TSP import *

if __name__ == "__main__":
    CITY_NUM = 10
    FILENAME = "TSP.csv"

    city = loadCity(FILENAME, CITY_NUM)
    adj = getAdjMatrix(city)
    order = greedyTSP(city, adj)
    score = evaluateOrder(order, adj)
    print(order, score)
    arbitrary2CityChange(order)
    score = evaluateOrder(order, adj)
    print(order, score)
    arbitrary3CityChange(order)
    score = evaluateOrder(order, adj)
    print(order, score)