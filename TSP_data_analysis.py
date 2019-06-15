from data_analysis import *
import matplotlib.pyplot as plt


##################### data analysis ############################################
# todo: standardlise data analysis
def draw_best_one(total_results, city, figure_name, show = False):
    best_solution = total_results[0][0][0]
    for i, method in enumerate(total_results):
        for one_run in method:
            if one_run[-1].score < best_solution.score:
                best_solution = one_run[-1]
                print("in %d, score = %f" % (i, best_solution.score))
    solution = Solution(best_solution.order, best_solution.score, best_solution.evaluation)
    toGraph(solution, city, os.getcwd(), figure_name, show=show)

def plot_generation_score(variations, files, method_labels, function_labels, xlim):
    for key in method_labels:
        plt.figure()
        for var, file in zip(variations, files):
            m = re.match(r'TSP-(\d)-(\d)-(\d)', file)
            method = m.group(1) + m.group(3)
            function = m.group(2)
            if method == key:
                plt.plot(var["generation"], var["score"], drawstyle='steps-post', label=function_labels[function])
        plt.title(method_labels[key])
        plt.legend()
        plt.xlim(-100, xlim)
        plt.yscale("log")
        plt.show()

def plot_statics(data_table, labels, funcs):
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

FILENAME = "TSP.csv"
CITY_NUM = 100
BEST_TOUR = "best_tour"
REPEAT = 100
DATA_PATH = "\\..\\data\\TSP\\"
method_labels = {'00': "greedy firstMove", '01': "greedy bestMove",
                 '10': "random firstMove", '11': "random bestMove"}
function_labels = {'0': 'adjacent_2_item_change', '1': 'arbitrary_2_item_change',
                   '2': 'arbitrary_3_item_change', '3': 'insertion', '4': 'inversion',
                   '5': 'two_times_inversion'}
files = os.listdir(os.getcwd() + DATA_PATH)
total_results = get_row_data(DATA_PATH)
data_table = to_table(total_results, files)
generation_score = vary_of_generation(total_results, files)
plot_generation_score(generation_score, files, method_labels, function_labels)