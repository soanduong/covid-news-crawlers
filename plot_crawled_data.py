# -*- coding: utf-8 -*-
"""
Created on 25/02/2021 11:35 pm

@author: Soan Duong, UOW
"""
# Standard library imports
import json
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

# Read the crawled data
from tqdm import tqdm


# ------------------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    args = argparse.ArgumentParser(description='Main file')
    args.add_argument('--site_name', default='laodong', type=str,
                      help='Name of the online newspaper, e.g. vnexpress and laodong.')
    args.add_argument('--out_dir', default='figs/', type=str,
                      help='Directory for saving the output plot')
    cmd_args = args.parse_args()

data = []
with open(f'data/{cmd_args.site_name}.jsonl') as f:
    for line in f:
        data.append(json.loads(line))
data_unique = list({v['url']:v for v in data}.values())

# Set the date range
date_start = '2019-11-17'
date_end = '2021-01-01'
date_list = pd.date_range(date_start, date_end).tolist()

n_articles = []
for cur_date in tqdm(date_list, f'Counting news on {cmd_args.site_name}'):
    n_articles.append(len([item for item in data_unique
                           if item['date'] == cur_date.strftime('%Y-%m-%d')]))

# Smooth the actual curve
n_articles_smooth = savgol_filter(n_articles, 35, polyorder=3)

# Plot the results
fig = plt.figure(1, (15, 6))
linewidth = 2
plt.rcParams.update({'font.size': 24})
plt.rc('grid', linestyle="--", color='lightgray')
plt.plot(date_list, n_articles, 'lightsalmon', linewidth=linewidth,
         linestyle='--', label='Actual numbers')
plt.plot(date_list, n_articles_smooth, 'r', linewidth=linewidth,
         label='Third-order smoothness')
plt.legend()
plt.xlabel('Timeline')
plt.ylabel('No. news')
plt.grid(True)
fig.tight_layout()
plt.xticks([date_list[0], date_list[-1]])
plt.savefig(f'{cmd_args.out_dir}/plot_{cmd_args.site_name}.png', dpi=300, bbox_inches='tight')
plt.show()