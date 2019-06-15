from FlowShop import *
from hyper_heuristic import *
from multiprocessing import Pool

def hyper_task(solution, funcs, firstMove, filename, kw):
    Solution.score_matrix = kw['matrix']
    Solution.fitness = kw['fitness']
    print("%s is running..." % (filename))
    start = time.time()
    iter_pop, bestSoFar = iterative_online_choice(kw['evaluations'], solution, funcs, firstMove)
    using_time = time.time() - start
    tofile(filename, iter_pop, using_time)

# basic setting
sub_dir = "data/FS/"
prefix = "FS-std-"
files = [('tai20_5.txt', 20, 5), ('tai100_10.txt', 100, 10), ('tai200_20.txt', 200, 20)]
record_step = 50
evaluation_bound = 500000
init_method = [johnson_greedy_order, random_order]
funcs = [adjacent_2_item_change, arbitrary_2_item_change, inversion, insertion]
funcs_del_adj = [adjacent_2_item_change, arbitrary_2_item_change_del_adj, inversion_del_adj, insertion_del_adj]
moveMethod = [True, False]
for k in range(10):
    process_pool = Pool(4)
    for e, file in enumerate(files):
        # p = np.loadtxt(file, delimiter=',')
        p = load_data(*file)
        key = {'matrix': p, 'fitness': makespan,
               'record_step': record_step, 'evaluations': evaluation_bound}
        Solution.score_matrix = p.copy()
        Solution.fitness = makespan
        for i in range(len(init_method)):
            for m in range(len(moveMethod)):
                # 对比 drill 和 drill_reduce
                filename = sub_dir + prefix + "%d-%d-9-%d.txt" % (e, i, m)
                print(filename)
                solution = Solution(init_method[i](p.copy()))
                process_pool.apply_async(hyper_task, args=(solution, funcs,
                                                           moveMethod[m], filename, key))
                filename = sub_dir + prefix + "%d-%d-8-%d.txt" % (e, i, m)
                process_pool.apply_async(hyper_task, args=(solution, funcs_del_adj,
                                                           moveMethod[m], filename, key))
    process_pool.close()
    process_pool.join()
