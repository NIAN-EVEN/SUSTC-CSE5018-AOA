from TSP import *

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

def randomOrder(cityNum):
    order = np.random.permutation(list(range(cityNum)))
    return order.tolist()