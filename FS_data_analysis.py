from FlowShop import *
from data_analysis import *
import matplotlib.pyplot as plt

def plot_generation_score(variations, prefix, files, method_labels, function_labels, xlim, group):
    for key in method_labels:
        plt.figure()
        for var, file in zip(variations, files):
            format = prefix + r'(\d)-(\d)-(\d)-(\d)'
            m = re.match(format, file)
            if m == None:
                continue
            method = m.group(2) + m.group(4)
            function = m.group(3)
            if method == key and m.group(1)==group:
                # plt.plot(var["generation"], var["score"], drawstyle='steps-post', label=function_labels[function])
                plt.plot(var["generation"], var["score"], label=function_labels[function])
        plt.title(method_labels[key])
        plt.legend()
        plt.xlim(-100, xlim)
        # plt.xscale('log')
        # plt.yscale("log")
        plt.show()



def wanted_file(filename):
    format = prefix + r'(.+).txt'
    m = re.match(format, filename)
    return m is not None



if __name__ == "__main__":

    DATA_PATH = "\\data\\FS\\"
    prefix = "FS-std-"
    # prefix = "hyper_heuristic_simple_order-"
    data_labels = {'0': '20_job_5_machine', '1': '100_job_10_machine', '2': '200_job_20_machine'}
    method_labels = {'00': "greedy firstMove", '01': "greedy bestMove",
                     '10': "random firstMove", '11': "random bestMove"}
    function_labels = {'0': 'adjacent_2_item_change', '1': 'arbitrary_2_item_change',
                       '2': 'arbitrary_3_item_change', '3': 'insertion', '4': 'inversion',
                       '5': 'two_times_inversion', '8': "drill_reduce", '9': 'drill'}

    files = list(filter((wanted_file) ,os.listdir(os.getcwd() + DATA_PATH)))
    total_results = get_row_data(DATA_PATH, prefix)
    data_table = to_table(total_results, files)
    generation_score = vary_of_generation(total_results, files)
    plot_generation_score(generation_score, prefix, files, method_labels, function_labels, xlim=500000, group='1')
