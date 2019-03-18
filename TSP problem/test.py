from greedy import *
from localSearch import *
from TSP import *

def contrastLocalSearch(initSolution, adj, generation, func):
    recordSolution = [initSolution]
    bestSolution = initSolution
    for i in range(generation):
        curOrder = bestSolution.order
        newOrder = func(curOrder)
        newSolution = Solution(newOrder, adj)
        recordSolution.append(newSolution)
        if newSolution.score < bestSolution.score:
            bestSolution = newSolution
    print("bestSolution in ADJ2CC: ", bestSolution)
    tofile(INIT_METHOD+func.__name__+TIME, recordSolution)

def expOnIterLocalSearch(initSolution, adj, iterNum):
    pop = iterativeLocalSearch(initSolution, adj, iterNum)
    tofile(INIT_METHOD+iterativeLocalSearch.__name__+str(iterNum), pop)

if __name__ == "__main__":
    # CITY_NUM = 100
    # FILENAME = "TSP.csv"
    # GENERATION = 100
    # INIT_METHOD = "greedy"
    FILENAME = sys.argv[1]
    CITY_NUM = int(sys.argv[2])
    GENERATION = int(sys.argv[3])
    INIT_METHOD = sys.argv[4]
    TIME = sys.argv[5]
    PROCESS_NUM = int(sys.argv[6])

    city = loadCity(FILENAME, CITY_NUM)
    adj = getAdjMatrix(city)
    if INIT_METHOD == "greedyInit":
        solution = Solution(greedyTSP(city, adj), adj)
    else:
        solution = Solution(randomOrder(CITY_NUM), adj)
    funcs = [adjacent2CityChange, arbitrary2CityChange, insertion, inversion, arbitrary3CityChange, twoTimesInversion]
    for func in funcs:
        print("on processing ", func.__name__)
        contrastLocalSearch(solution, adj, GENERATION, func)
    if not os.path.exists(INIT_METHOD+iterativeLocalSearch.__name__+str(GENERATION)):
        print("on processing ", expOnIterLocalSearch.__name__)
        expOnIterLocalSearch(solution, adj, GENERATION)