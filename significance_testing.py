import numpy as np
import pickle
from scipy import stats


def t_test(data, methods=['method_1', 'method3'], threshold=0.1):
    for enemy in data.keys():
        pop_1 = np.asarray(data[enemy][methods[0]])
        pop_2 = np.asarray(data[enemy][methods[1]])
        t_value, p_value = stats.ttest_ind_from_stats(pop_1.mean(), pop_1.std(), len(pop_1),
                                                      pop_2.mean(), pop_2.std(), len(pop_2), equal_var=False)
        print("t-value: ", t_value)
        print("p-value: ", p_value)
        if p_value < threshold:
            print("Difference for enemy {} is significant with threshold of {}.".format(enemy, threshold))
        else:
            print("Difference for enemy {} is NOT significant with threshold of {}.".format(enemy, threshold))


if __name__ == "__main__":
    data = pickle.load(open("best_ind_results", "rb"))
    t_test(data)
