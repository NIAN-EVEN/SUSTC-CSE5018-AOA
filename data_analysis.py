from local_search import *
import matplotlib.pyplot as plt
import os, re
import pandas as pd

def get_row_data(data_path, prefix):
    files = os.listdir(os.getcwd() + data_path)
    tuples = {}
    for i, file in enumerate(files):
        format = prefix + r'(.+).txt'
        m = re.match(format, file)
        if m != None:
            print("%d: %s" % (i, file))
            group = m.group(1)
            one_tuple = []
            run = []
            with open(os.getcwd() + data_path + file, 'r') as f:
                for line in f.readlines():
                    if line == '\n':
                        continue
                    if line[0] == 'u':
                        one_tuple.append(run)
                        run = []
                    else:
                        m = re.match(r'^evaluation=(\d+), score=(\d+), order=(.+)', line)
                        dt = Solution(eval(m.group(3)), int(m.group(2)), int(m.group(1)))
                        run.append(dt)
            one_tuple.pop(0)
            tuples[group] = one_tuple
    return tuples

def to_table(total_record, files):
    worest_score_record = []
    best_score_record = []
    mean_score_record = []
    for key, method in total_record.items():
        best_solution = method[0][0]
        worest_solution = method[0][-1]
        total_score = 0
        for one_run in method:
            total_score += one_run[-1].score
            if one_run[-1].score < best_solution.score:
                best_solution = one_run[-1]
            if one_run[-1].score > best_solution.score:
                worest_solution = one_run[-1]
        mean_score = total_score / len(method)
        worest_score_record.append(worest_solution.score)
        best_score_record.append(best_solution.score)
        mean_score_record.append(mean_score)
    data = {"best_score": best_score_record,
            "mean_score": mean_score_record,
            "worest_score": worest_score_record}
    table = pd.DataFrame(data, index=files)
    return table

def vary_of_generation(row_data, files):
    '''对于每种方法, 统计最多的记录了几代, 将该代数作为横坐标，
    没有中间代的使用小于等于该代数的得分作为该代得分'''
    max_generation = 0
    for key, method in row_data.items():
        for one_run in method:
            solutions = one_run[-1]
            if solutions.evaluation_num > max_generation:
                max_generation = solutions.evaluation_num
    variations = []
    for key, method in row_data.items():
        generations = []
        for one_run in method:
            for solution in one_run:
                if solution.evaluation_num not in generations:
                    generations.append(solution.evaluation_num)
        generations.sort()
        score_record = []
        for g in generations:
            total_score = 0
            # 统计所有run的均值
            for one_run in method:
                if one_run[-1].evaluation_num < g:
                    total_score += one_run[-1].score
                    continue
                for solution in one_run:
                    if solution.evaluation_num >= g:
                        total_score += solution.score
                        break
            mean_score = total_score / len(method)
            score_record.append(mean_score)
        generations.append(max_generation)
        score_record.append(score_record[-1])
        dct = {"generation": generations,
               "score": score_record}
        table = pd.DataFrame(dct)
        variations.append(table)
    return variations

def get_time_of_each_run(data_path, prefix):
    files = os.listdir(os.getcwd() + data_path)
    tuples = {}
    for i, file in enumerate(files):
        format = prefix + r'(.+).txt'
        m = re.match(format, file)
        if m != None:
            print("%d: %s" % (i, file))
            group = m.group(1)
            one_tuple = []
            run = []
            with open(os.getcwd() + data_path + file, 'r') as f:
                total_time = 0
                repeat = 0
                for line in f.readlines():
                    m = re.match(r'using time = ([\d+]\.[\d+])')
                    if m != None:
                        total_time += float(m.group(1))
                        repeat += 1
                mean_time = total_time / repeat
            print(file, ":", mean_time)

# def plot_substatics(data_table, labels):
#     for combi in combinations(labels, 2):
#         plt.figure()
#         step_width = 0.4
#         sigle_width = 0.2
#         xticks = np.arange(len(funcs))
#         j = 0
#         for i, label in enumerate(labels):
#             if label == combi[0] or label == combi[1]:
#                 x = xticks + j * step_width
#                 y = np.array(data_table["mean_score"][i:len(data_table):len(labels)])
#                 plt.bar(x, y, label=label, width=sigle_width, align="center")
#                 for a, b in zip(x, y):
#                     plt.text(a, b, "%d"% b, horizontalalignment='center', verticalalignment="baseline", fontsize=10)
#                 j += 1
#         plt.xticks(xticks+sigle_width/2, labels=[func.__name__ for func in funcs], fontsize=10, rotation=15)
#         plt.ylim(ymin=7000)
#         plt.legend()
#         plt.show()

if __name__ == "__main__":
    FILENAME = "TSP.csv"
    CITY_NUM = 100
    BEST_TOUR = "best_tour"
    DATA_PATH = "\\data\\TSP\\"
    data_labels = {'0':'20_job_5_machine', '1':'100_job_10_machine'}
    method_labels = {'00':"greedy firstMove", '01':"greedy bestMove",
              '10':"random firstMove", '11':"random bestMove"}
    function_labels = {'0':'adjacent_2_item_change', '1':'arbitrary_2_item_change',
                       '2':'arbitrary_3_item_change', '3':'insertion', '4':'inversion',
                       '5':'two_times_inversion'}

    files = os.listdir(os.getcwd() + DATA_PATH)
    total_results = get_row_data(DATA_PATH)
    data_table = to_table(total_results, files)
    generation_score = vary_of_generation(total_results, files)
