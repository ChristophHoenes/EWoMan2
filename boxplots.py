import pickle as pkl
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd



with open("best_ind_results", "rb") as f:
    data = pkl.load(f)
print(data)
sns.set_theme(style="whitegrid")
enemies = [2, 6,7]
#df2 =
#df = pd.DataFrame.from_dict(data[2])
for enemy in enemies:
    if enemy==2:
        df = pd.DataFrame.from_dict(data[enemy])
        df['enemy'] = enemy
        values = df['method_1'].tolist()
        values.extend(df['method3'].tolist())
        df2 = pd.DataFrame({'individual gain': values})
        df2['enemy'] = enemy
        df2['method'] = 0
        df2.loc[:10, 'method'] = 1
        df2.loc[10:, 'method'] = 2
    else:
        df = pd.DataFrame.from_dict(data[enemy])
        df['enemy'] = enemy
        values = df['method_1'].tolist()
        values.extend(df['method3'].tolist())
        sub_df2 = pd.DataFrame({'individual gain': values})
        sub_df2['enemy'] = enemy
        sub_df2['method'] = 0
        sub_df2.loc[:10, 'method'] = 1
        sub_df2.loc[10:, 'method'] = 2
        #print(sub_df2)
        df2 = df2.append(sub_df2, ignore_index=True)

print(df2.head(60))

sns.set_theme(font_scale=2)
ax = sns.boxplot(x="enemy", y="individual gain", hue="method",
                 data=df2, palette="Set2")
fig = ax.get_figure()
fig.savefig('boxplots.png', bbox_inches='tight')

