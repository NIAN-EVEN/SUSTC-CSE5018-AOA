from local_search import *
from TSP import *
import matplotlib.pyplot as plt
import os
import pandas as pd

def get_row_data(filename, city_num, data_path):
    city = loadCity(filename, city_num)
    adj = getAdjMatrix(city)
    files = os.listdir(os.getcwd() + data_path)
    total_results = []
    for i, file in enumerate(files):
        print("%d: %s" % (i, file))
        result = []
        with open(os.getcwd() + DATA_PATH + file, 'r') as f:
            line = f.readline()
            while line:
                while line == "\n":
                    line = f.readline()
                    if len(group) != 0:
                        result.append((group, time))
                        group = []
                if not line:
                    break
                if line.find("using") != -1:
                    time = float(line[12:20])
                    group = []
                    line = f.readline()
                info = line.strip().split('|')
                order = eval(info[0])
                solution = Solution(order, adj)
                solution.generation = eval(info[1])
                group.append(solution)
                line = f.readline()
        total_results.append(result)
    return total_results

def to_table(total_record, files):
    worest_score_record = []
    best_score_record = []
    mean_score_record = []
    mean_time_record = []
    mean_generation_record = []
    for i, method in enumerate(total_record):
        best_solution = method[0][0][-1]
        worest_solution = method[0][0][-1]
        total_score = 0
        total_time = 0
        total_generation = 0
        for one_run in method:
            total_time += one_run[1]
            total_generation += one_run[0][-1].generation
            total_score += one_run[0][-1].score
            if one_run[0][-1].score < best_solution.score:
                best_solution = one_run[0][-1]
            if one_run[0][-1].score > best_solution.score:
                worest_solution = one_run[0][-1]
        # best_solution.toGraph(city, os.getcwd(), files[i], show=False)
        mean_time = total_time / len(method)
        mean_score = total_score / len(method)
        mean_time_record.append(mean_time)
        mean_generation_record.append(total_generation / len(method))
        worest_score_record.append(worest_solution.score)
        best_score_record.append(best_solution.score)
        mean_score_record.append(mean_score)
    data = {"best_score": best_score_record,
            "mean_score": mean_score_record,
            "worest_score": mean_score_record,
            "mean_time": mean_time_record,
            "mean_generation": mean_generation_record}
    table = pd.DataFrame(data, index=files)
    return table

def draw_best_one(total_results, figure_name, show = False):
    best_solution = total_results[0][0][0][0]
    for i, method in enumerate(total_results):
        for one_run in method:
            if one_run[0][-1].score < best_solution.score:
                best_solution = one_run[0][-1]
                print("in %d, score = %f" % (i, best_solution.score))
    best_solution.toGraph(city, os.getcwd(), figure_name, show)

def vary_of_generation(row_data, files):
    '''对于每种方法, 统计最多的记录了几代, 将该代数作为横坐标，
    没有中间代的使用小于等于该代数的得分作为该代得分'''
    max_generation = 0
    for file, method in zip(files, row_data):
        for one_run in method:
            solutions = one_run[0]
            if solutions[-1].generation > max_generation:
                max_generation = solutions[-1].generation
    variations = []
    for file, method in zip(files, row_data):
        max_record_length = 0
        generations = []
        for one_run in method:
            solutions = one_run[0]
            if len(solutions) > max_record_length:
                max_record_length = len(solutions)
                generations = [g.generation for g in solutions]
        score_record = []
        for g in generations:
            total_score = 0
            # 统计每个generation的100次平均得分
            for one_run in method:
                solutions = one_run[0]
                for i in range(len(solutions)):
                    if i + 1 == len(solutions) or solutions[i].generation >= g:
                        total_score += solutions[i].score
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

def plot_generation_score(variations, labels):
    step = len(labels)
    for i in range(step):
        plt.figure()
        for j, var in enumerate(variations[i::step]):
            plt.plot(var["generation"], var["score"], drawstyle='steps-post', label=funcs[j].__name__)
        plt.title(labels[i])
        plt.legend()
        plt.xscale("log")
        plt.show()

def plot_statics(data_table, labels):
    plt.figure()
    sigle_width = 0.2
    xticks = np.arange(len(funcs))
    for i, label in enumerate(labels):
        plt.bar(xticks + i * sigle_width, data_table["mean_score"][i:len(data_table):len(labels)],
                label=label, width=sigle_width, align="center")
    plt.xticks(xticks + 0.3, labels=[func.__name__ for func in funcs], rotation=20)
    plt.ylim(ymin=7000)
    plt.legend()
    plt.show()

def plot_substatics(data_table, labels):
    for combi in combinations(labels, 2):
        plt.figure()
        step_width = 0.4
        sigle_width = 0.2
        xticks = np.arange(len(funcs))
        j = 0
        for i, label in enumerate(labels):
            if label == combi[0] or label == combi[1]:
                x = xticks + j * step_width
                y = np.array(data_table["mean_score"][i:len(data_table):len(labels)])
                plt.bar(x, y, label=label, width=sigle_width, align="center")
                for a, b in zip(x, y):
                    plt.text(a, b, "%d"%b, horizontalalignment='center', verticalalignment="baseline", fontsize=10)
                j += 1
        plt.xticks(xticks+sigle_width/2, labels=[func.__name__ for func in funcs], fontsize=10, rotation=15)
        plt.ylim(ymin=7000)
        plt.legend()
        plt.show()

if __name__ == "__main__":
    FILENAME = "TSP.csv"
    CITY_NUM = 100
    BEST_TOUR = "best_tour"
    DATA_PATH = "\\localsearch_data\\"
    labels = ["greedy bestMove", "greedy firstMove", "random bestMove", "random firstMove"]

    files = os.listdir(os.getcwd() + DATA_PATH)
    total_results = get_row_data(FILENAME, CITY_NUM, DATA_PATH)
    data_table = to_table(total_results, files)
    generation_score = vary_of_generation(total_results, files)


