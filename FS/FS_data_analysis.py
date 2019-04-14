from FS import *

def plot_generation_score(variations, files, method_labels, function_labels, xlim):
    for key in method_labels:
        plt.figure()
        for var, file in zip(variations, files):
            m = re.match(r'FS-(\d)-(\d)-(\d)-(\d)', file)
            if m == None:
                continue
            method = m.group(2) + m.group(4)
            function = m.group(3)
            if method == key and m.group(1)=='1':
                # plt.plot(var["generation"], var["score"], drawstyle='steps-post', label=function_labels[function])
                plt.plot(var["generation"], var["score"], label=function_labels[function])
        plt.title(method_labels[key])
        plt.legend()
        plt.xlim(-100, xlim)
        # plt.xscale('log')
        # plt.yscale("log")
        plt.show()



DATA_PATH = "\\..\\data\\FS\\"
data_labels = {'0': '20_job_5_machine', '1': '100_job_10_machine'}
method_labels = {'00': "greedy firstMove", '01': "greedy bestMove",
                 '10': "random firstMove", '11': "random bestMove"}
function_labels = {'0': 'adjacent_2_item_change', '1': 'arbitrary_2_item_change',
                   '2': 'arbitrary_3_item_change', '3': 'insertion', '4': 'inversion',
                   '5': 'two_times_inversion'}

files = os.listdir(os.getcwd() + DATA_PATH)
total_results = get_row_data(DATA_PATH)
data_table = to_table(total_results, files)
generation_score = vary_of_generation(total_results, files)
plot_generation_score(generation_score, files, method_labels, function_labels, xlim=3000)
# 首先获取全部数据
# 然后单独存储需要对比的数据
# 对数据做后期处理
# 出图