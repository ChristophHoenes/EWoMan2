import numpy as np
import pickle
from scipy import stats



def t_test(data, methods=['scalarization', 'nsga2_3'], threshold=0.1):

    gains_method1 = []
    gains_method2 = []
    for enemy in data.keys():
        gains_method1.append([tup[0] - tup[1] for tup in data[enemy][methods[0]]])
        gains_method2.append([tup[0] - tup[1] for tup in data[enemy][methods[1]]])
        #pop_1 = np.asarray(data[enemy][methods[0]])
        #pop_2 = np.asarray(data[enemy][methods[1]])

    pop_1 = np.asarray(list(map(sum, zip(*gains_method1))))
    pop_2 = np.asarray(list(map(sum, zip(*gains_method2))))

    t_value, p_value = stats.ttest_ind_from_stats(pop_1.mean(), pop_1.std(ddof=1), len(gains_method1[0]),
                                                  pop_2.mean(), pop_2.std(ddof=1), len(gains_method2[0]), equal_var=False)
    print("t-value: ", t_value)
    print("p-value: ", p_value)
    if p_value < threshold:
        print("Difference for enemy {} is significant with threshold of {}.".format(enemy, threshold))
    else:
        print("Difference for enemy {} is NOT significant with threshold of {}.".format(enemy, threshold))


if __name__ == "__main__":
    data = pickle.load(open("results/best_ind_results_enemy1_2_5", "rb"))
    t_test(data)
