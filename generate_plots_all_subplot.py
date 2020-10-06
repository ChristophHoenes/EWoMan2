import pickle
import numpy as np
from matplotlib import pyplot as plt


def plot_stat_mean(stat_key='mean', methods=['method_1', 'method3'], enemy=2, seeds=None, prefix=None, fancy=False, savepath=''):
    

    enemy_list = [2,6,7]


    plt.figure()
    ind_count = 310
    for index,enemy in enumerate(enemy_list):
        print(enemy)
        runs = []
        max_list = []


        if seeds is None:
            seeds = [111, 222, 333, 444, 555, 666, 777, 888, 999, 1010]
        for method in methods:
            if method == 'method_1':
                prefix = 'roundrobin'
            elif method == 'method3':
                prefix = 'diversity_075_roundrobin'
            for seed in seeds:
                log_path = 'results/{}/{}_enemy{}_seed_{}/logs_iter_30'.format(method, prefix, enemy, seed)
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
                if method =='method_1':
                    m = 'm1'
                    color = 'magenta'
                    ind_count = ind_count + 1 
                    print(ind_count)

                    plt.subplot(ind_count).set_title('Results for ' + ylab + ' enemy %d' % (enemy))
                else:
                    m = 'm2'
                    color = 'green'
                if stat_key == 'mean': 
                    legend_label = 'mean '
                    
                    #If you want to get the max, use these error bars and comment the other one out.
                    plt.errorbar(np.arange(len(mean)), max_mean, max_std, alpha=.75, fmt=':', capsize=3, capthick=1, label = 'max '+ m,color=color)
                    plt.fill_between(np.arange(len(mean)), max_mean-max_std, max_mean+max_std, alpha=.25,color=color)

                #If you want to get the mean of either the diversity or fitness, use these error bars and comment the other one out.
                '''plt.errorbar(np.arange(len(mean)), mean, std, alpha=.75, fmt=':', capsize=3, capthick=1, label = legend_label+ m)
                plt.fill_between(np.arange(len(mean)), mean-std, mean+std, alpha=.25)'''
                plt.legend(loc='best', shadow=True, fontsize='x-small')
                
                plt.ylabel(ylab)
                plt.xlabel('iteration')
                
                plt.rcParams["font.size"] = "10"
                
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
    
    #plot_stat_mean(stat_key='diversity', enemy=0, fancy=True,savepath='plots/all_diversity_enemy')
    
    plot_stat_mean(stat_key='mean', enemy=7, fancy=True,savepath='plots/fitness_enemy_max')
    
    #plot_diversity(logs)
