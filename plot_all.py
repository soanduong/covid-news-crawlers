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
site_names = ['laodong', '24h', 'kenh14', 'dantri', 'cafef',
              'vnexpress', 'tuoitre', 'vietnamnet', 'zingnews', 'thanhnien']

# Set the date range
date_start = '2020-01-01'
date_end = '2020-12-31'
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
# plt.xlabel('Timeline')
plt.ylabel('No. news')
plt.grid(True)
fig.tight_layout()
# plt.xlabel('Timeline') date_list[63],
plt.xticks([date_list[0], date_list[22], date_list[113],
            date_list[204], date_list[224], date_list[-1]],
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
# plt.xlabel('Timeline') date_list[63],
plt.xticks([date_list[0], date_list[22], date_list[113],
            date_list[204], date_list[224], date_list[-1]],
           rotation=rotation)
plt.xlim([date_list[0], date_list[-1]])
plt.savefig(f'figs/plot_gradient.png', dpi=300, bbox_inches='tight')
plt.show()
