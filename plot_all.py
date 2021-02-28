# -*- coding: utf-8 -*-
"""
Created on 26/02/2021 12:48 pm

@author: Soan Duong, UOW
"""
# Standard library imports
import numpy as np

# Third party imports
import torch

# Local application imports

# Standard library imports
import json
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

# Read the crawled data
from tqdm import tqdm

# Set the site names
site_names = ['laodong', '24h', 'kenh14', 'dantri', 'cafef', 'vnexpress']

# Set the date range
date_start = '2019-11-17'
date_end = '2021-01-01'
date_list = pd.date_range(date_start, date_end).tolist()
# date_list_display = [item.strftime('%d/%m/%y') for item in date_list]
# date_list_display = [item.strftime('%d/%m') for item in date_list]
date_list_txt = [item.strftime('%Y-%m-%d') for item in date_list]

# Count the number of covid-19 related articles in each site
n_articles_list = np.zeros(len(date_list))
for site_name in site_names:
    data = []
    with open(f'data/{site_name}.jsonl') as f:
        for line in f:
            data.append(json.loads(line))
    data_unique = list({v['url']:v for v in data}.values())
    print(f'\nTotal number of covid-19 related articles in {site_name}: {len(data_unique)}')

    for k, cur_date in tqdm(enumerate(date_list_txt), f'Counting news on {site_name}'):
        n_articles_list[k] += len([item for item in data_unique
                                  if item['date'] == cur_date])
print(f'\nTotal number of covid-19 related articles in the '
      f'{len(site_names)} sites: {np.sum(n_articles_list):.0f}')

# Smooth the actual curve
n_articles_smooth = savgol_filter(n_articles_list, 35, polyorder=3)

date_list = [item.strftime('%d/%m/%Y') for item in date_list]
rotation = 20
fig_size = (15, 5)
fontsize = 20
# Plot the results
fig = plt.figure(1, fig_size)
linewidth = 2
plt.rcParams.update({'font.size': fontsize})
plt.rc('grid', linestyle="--", color='lightgray')
plt.plot(date_list, n_articles_list, 'lightsalmon', linewidth=linewidth,
         linestyle='--', label='Actual numbers')
plt.plot(date_list, n_articles_smooth, 'r', linewidth=linewidth,
         label='Third-order smoothness')
plt.legend()
plt.xlabel('Timeline')
plt.ylabel('No. news')
plt.grid(True)
fig.tight_layout()
plt.xticks([date_list[0], date_list[109], date_list[158],
            date_list[249], date_list[284], date_list[-1]],
           rotation=rotation)
plt.xlim([date_list[0], date_list[-1]])
plt.savefig(f'figs/plot_articles.png', dpi=300, bbox_inches='tight')
plt.show()

# Display the gradient of the smooth curve
fig = plt.figure(1, fig_size)
plt.rcParams.update({'font.size': fontsize})
plt.rc('grid', linestyle="--", color='lightgray')
grad_n_articles = np.zeros(len(n_articles_list))
grad_n_articles[1:] = (n_articles_smooth[1:] - n_articles_smooth[:-1])
plt.plot(date_list, grad_n_articles, 'dodgerblue', linewidth=2)
plt.ylabel('Gradient of the smoothness')

plt.grid(True)
plt.xlabel('Timeline')
plt.xticks([date_list[0], date_list[109], date_list[158],
            date_list[249], date_list[284], date_list[-1]],
           rotation=rotation)
plt.xlim([date_list[0], date_list[-1]])
plt.savefig(f'figs/plot_gradient.png', dpi=300, bbox_inches='tight')
plt.show()


# Display the all three curve (actual, smooth, and gradient)
plt.close()
fig = plt.figure(2, fig_size)
ax1 = plt.gca()
plt.rcParams.update({'font.size': fontsize})
plt.rc('grid', linestyle="--", color='lightgray')
ax1.plot(date_list, n_articles_list, 'lightsalmon',
         linewidth=linewidth, linestyle='--', label='Actual numbers')
ax1.plot(date_list, n_articles_smooth, 'r', linewidth=linewidth,
         label='Third-order smoothness')

# plt.legend()
plt.xticks([date_list[0], date_list[109], date_list[158],
            date_list[249], date_list[284], date_list[-1]],
           rotation=rotation)
ax2 = ax1.twinx()
ax2.plot(date_list, grad_n_articles, 'dodgerblue',
         linewidth=2, label='Gradient of smoothness')

# plt.legend()
ax1.grid()
plt.xticks([date_list[0], date_list[109], date_list[158],
            date_list[249], date_list[284], date_list[-1]],
           rotation=rotation)
ax1.set_xlabel('Timeline')
ax1.set_ylabel('No. news', color='tab:red')
ax2.set_ylabel('Gradient of the smoothness', color='dodgerblue')
ax1.set_xlim([date_list[0], date_list[-1]])
fig.legend(loc="upper center", bbox_to_anchor=(0.45, 1.03),
           ncol=3, fancybox=True)
plt.savefig(f'figs/plot_all.png', dpi=300, bbox_inches='tight')
plt.show()