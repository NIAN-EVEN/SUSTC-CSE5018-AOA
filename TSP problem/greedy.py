from TSP import *

def greedyTSP(city, adj):
    cityNum = len(city)
    order = [np.random.randint(0, cityNum)]
    for i in range(cityNum-1):
        options = adj[order[-1]]
        nextDistance = sys.float_info.max
        for idx, value in enumerate(options):
            if idx != order[-1] and order.count(idx)==0 and value < nextDistance:
                nextCity = idx
                nextDistance = value
        order.append(nextCity)
    errorDetect(order)
    return order