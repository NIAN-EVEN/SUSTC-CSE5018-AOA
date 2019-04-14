from TSP.TSP import *
import matplotlib.pyplot as plt
import os, re
import pandas as pd

def get_row_data(data_path, repeat):
    files = os.listdir(os.getcwd() + data_path)
    tuples = []
    for i, file in enumerate(files):
        print("%d: %s" % (i, file))
        one_tuple = []
        run = []
        with open(os.getcwd() + DATA_PATH + file, 'r') as f:
            for line in f.readlines():
                if line == '\n':
                    continue
                if line[0] == 'u':
                    one_tuple.append(run)
                    run = []
                else:
                    m = re.match(r'^evaluation=(\d+), score=(\d+), order=(.+)', line)
                    dt = {'e':int(m.group(1)), 's':int(m.group(2)), 'o':m.group(3)}
                    run.append(dt)
        one_tuple.pop(0)
        tuples.append(one_tuple)
    return tuples

def to_table(total_record, files):
    worest_score_record = []
    best_score_record = []
    mean_score_record = []
    for i, method in enumerate(total_record):
        best_solution = method[0][0]
        worest_solution = method[0][0]
        total_score = 0
        for one_run in method:
            total_score += one_run[-1]['s']
            if one_run[-1]['s'] < best_solution['s']:
                best_solution = one_run[-1]
            if one_run[-1]['s'] > best_solution['s']:
                worest_solution = one_run[-1]
        mean_score = total_score / len(method)
        worest_score_record.append(worest_solution['s'])
        best_score_record.append(best_solution['s'])
        mean_score_record.append(mean_score)
    data = {"best_score": best_score_record,
            "mean_score": mean_score_record,
            "worest_score": mean_score_record}
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
            solutions = one_run[-1]
            if solutions['e'] > max_generation:
                max_generation = solutions['e']
    variations = []
    for file, method in zip(files, row_data):
        generations = []
        for one_run in method:
            for solution in one_run:
                if solution['e'] not in generations:
                    generations.append(solution['e'])
        generations.sort()
        score_record = []
        for g in generations:
            total_score = 0
            # 统计每个generation的100次平均得分
            for one_run in method:
                if one_run[-1]['e'] < g:
                    total_score += one_run[-1]['s']
                    continue
                for solution in one_run:
                    if solution['e'] >= g:
                        total_score += solution['s']
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
        plt.yscale("log")
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
    REPEAT = 100
    DATA_PATH = "\\data\\TSP\\"
    labels = ["greedy bestMove", "greedy firstMove", "random bestMove", "random firstMove"]

    files = os.listdir(os.getcwd() + DATA_PATH)
    total_results = get_row_data(DATA_PATH, REPEAT)
    data_table = to_table(total_results, files)
    generation_score = vary_of_generation(total_results, files)


