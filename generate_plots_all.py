import pickle
import numpy as np
from matplotlib import pyplot as plt


def plot_stat_mean(stat_key='mean', methods=('scalarization', 'nsga2_2'), enemy=(1, 2, 5), seeds=None, prefix=None, fancy=False, savepath=''):
    runs = []
    max_list = []
    if seeds is None:
        seeds = [111, 222, 333, 444, 555, 666, 777, 888, 999, 1010]

    enemies_str = ("{}" + "_{}" * (len(enemy) - 1)).format(*enemy)

    for method in methods:
        if method == 'scalarization':
            prefix = 'scalarization'
        elif method == 'nsga2' or method == 'nsga2_2':
            prefix = 'nsga2'
        for seed in seeds:
            log_path = 'results/{}/{}_enemy{}_seed_{}/logs_iter_100'.format(method, prefix, enemies_str, seed)
            logs = pickle.load(open(log_path, "rb"))
            runs.append([step[stat_key] for step in logs[0]])
            if stat_key == 'mean':
                max_list.append([step['max'] for step in logs[0]])
        np_runs = np.asarray(runs)
        np_max = np.asarray(max_list)
        if stat_key == 'diversity':
            np_runs /= 100 * 265
            ylab = 'diversity'
        else:
            ylab = 'fitness'
            max_mean = np_max.mean(axis=0)
            max_std = np_max.std(axis=0)
        mean = np_runs.mean(axis=0)
        std = np_runs.std(axis=0)

        
        if fancy:
            legend_label = ''

            if method =='scalarization':
                m = 'm1'
                color = 'magenta'
            else:
                m = 'm2'
                color = 'green'
            if stat_key == 'mean': 
                legend_label = 'mean '
                plt.errorbar(np.arange(len(mean)), max_mean, max_std, alpha=.75, fmt=':', capsize=3, capthick=1, label = 'max '+ m,color=color)
                plt.fill_between(np.arange(len(mean)), max_mean-max_std, max_mean+max_std, alpha=.25,color=color)
            
            plt.errorbar(np.arange(len(mean)), mean, std, alpha=.75, fmt=':', capsize=3, capthick=1, label = legend_label+ m)
            plt.legend(loc='best', shadow=True, fontsize='x-small')
            plt.fill_between(np.arange(len(mean)), mean-std, mean+std, alpha=.25)
            plt.ylabel(ylab)
            plt.xlabel('iteration')
            plt.rcParams["font.size"] = "20"
            plt.suptitle('Results for ' + ylab + ' enemies {}'.format(enemies_str.replace('_',',')))
        else:
            plt.errorbar(np.arange(len(mean)), mean, std, linestyle='-', marker='o')

    if savepath == '':
        plt.show()
    else:
        plt.tight_layout()
        plt.savefig(savepath, bbox_inches="tight")
        plt.close()


def plot_stat(logs, stat_key='mean', savepath=''):
    diversities = [step[stat_key] for step in logs[0]]
    plt.plot(range(len(diversities)), diversities)
    if savepath == '':
        plt.show()
    else:
        plt.savefig(savepath)


if __name__ == "__main__":
    #plot_stat_mean(stat_key='diversity', enemy=7, fancy=True,savepath='plots/diversity_enemy7_new')
    #plot_stat_mean(stat_key='diversity', enemy=6, fancy=True,savepath='plots/diversity_enemy6_new')
    #plot_stat_mean(stat_key='diversity', enemy=2, fancy=True,savepath='plots/diversity_enemy2_new')

    plot_stat_mean(stat_key='mean', enemy=(1, 2, 5), fancy=True,savepath='plots/fitness_enemy1_2_5')
    plot_stat_mean(stat_key='mean', enemy=(2, 6, 7), fancy=True,savepath='plots/fitness_enemy2_6_7')
    #plot_stat_mean(stat_key='mean', enemy=2, fancy=True,savepath='plots/fitness_enemy2_new')
    #plot_diversity(logs)
