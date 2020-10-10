import pickle
import numpy as np
from matplotlib import pyplot as plt


def plot_stat_mean(stat_key='mean', methods=('scalarization', 'nsga2_2'), enemy=(1, 2, 5), seeds=None, prefix=None, fancy=False, savepath=''):
    runs = []
    if seeds is None:
        seeds = [111, 222, 333, 444, 555, 666, 777, 888, 999, 1010]

    enemies_str = ("{}" + "_{}" * (len(enemy) - 1)).format(*enemy)

    for method in methods:
        if method == 'scalarization':
            prefix = 'scalarization'
        elif method == 'nsga2':
            prefix = 'nsga2'
        elif method == 'nsga2_2':
            prefix = 'nsga2_2'
        for seed in seeds:
            log_path = 'results/{}/{}_enemy{}_seed_{}/logs_iter_100'.format(method, prefix, enemies_str, seed)
            logs = pickle.load(open(log_path, "rb"))
            runs.append([step[stat_key] for step in logs[0]])
        np_runs = np.asarray(runs)
        if stat_key == 'diversity':
            np_runs /= 100 * 265
        mean = np_runs.mean(axis=0)
        std = np_runs.std(axis=0)
        if fancy:
            plt.errorbar(np.arange(len(mean)), mean, std, alpha=.75, fmt=':', capsize=3, capthick=1)
            plt.fill_between(np.arange(len(mean)), mean-std, mean+std, alpha=.25)
        else:
            plt.errorbar(np.arange(len(mean)), mean, std, linestyle='-', marker='o')
    if savepath == '':
        plt.show()
    else:
        plt.savefig(savepath)


def plot_stat(logs, stat_key='mean', savepath=''):
    diversities = [step[stat_key] for step in logs[0]]
    plt.plot(range(len(diversities)), diversities)
    if savepath == '':
        plt.show()
    else:
        plt.savefig(savepath)


if __name__ == "__main__":
    #log_path = "results/method2/diversity_roundrobin_enemy2_seed_222/logs_iter_30"
    #logs = pickle.load(open(log_path, "rb"))
    #plot_stat(logs, stat_key='max')
    plot_stat_mean(stat_key='diversity', enemy=7, fancy=True)

