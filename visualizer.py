import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def process_data(li):
    block_arr = np.array(li)
    # 고유 값들 뽑아서

    unique_value = np.unique(block_arr)
    unique_value_count = []
    for unique in unique_value:
        unique_value_count.append(np.log(len(block_arr[block_arr == unique])))

    log_unique_value = np.log(unique_value)

    return log_unique_value, unique_value_count, np.log(block_arr)


def histogram(li):
    plt.title('Transaction Fee Histogram')
    x, y, block = process_data(li)
    sns.distplot(block, kde=True, hist=False, rug=True)
    plt.show()
