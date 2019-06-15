# todo: 文件夹和文件同名时会出现ModuleNotFoundError: No module named 'TSP.TSP'; 'TSP' is not a package
# from TSP.TSP import *
from multiprocessing import Pool
from local_search import *

def on_server():
    p = Pool()
    for s in range(CITY_NUM):
        for i in range(len(init_method)):
            for f in range(len(funcs)):
                for m in range(len(moveMethod)):
                    solution = Solution(init_method[i](city, adj, s))
                    filename = 'data/TSP/TSP-%d-%d-%d.txt' % (i, f, m)
                    p.apply_async(task, args=(solution, funcs[f], moveMethod[m],
                                              filename, key, True))
    # print("waitting for child process finish")
    p.close()
    p.join()

def dbg():
    for s in range(CITY_NUM):
        for i in range(1):
            for f in range(2, 3):
                for m in range(1, 2):
                    solution = Solution(init_method[i](city, adj, s))
                    filename = 'data/TSP/TSP-%d-%d-%d.txt' % (i, f, m)
                    task(solution, funcs[f], moveMethod[m], filename, key)

funcs = [adjacent_2_item_change, arbitrary_2_item_change, arbitrary_3_item_change,
         insertion, inversion, two_times_inversion]
init_method = [greedyTSP, randomTSP]
moveMethod = [True, False]
FILENAME = 'TSP.csv'
CITY_NUM = 100
city = loadCity(FILENAME, CITY_NUM)
adj = getAdjMatrix(city)
key = {'matrix':adj, 'fitness':tour_length,
       'record_step':50, 'evaluations':500000}
Solution.score_matrix = adj
Solution.fitness = tour_length
dbg()
# on_server()