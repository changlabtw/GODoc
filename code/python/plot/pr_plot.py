import os
import re
import sys
import time
import glob
import pandas
import argparse
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.legend_handler import HandlerLine2D

def process_options():
    global args

    parser = argparse.ArgumentParser(description='Plot cumulative of pixel difference count')
    parser.add_argument('-i', '--input', type=str, required=True, nargs='*', help='Data')
    parser.add_argument('-t', '--title', type=str, required=True, help='Figure title')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output')

    args = parser.parse_args()

    for f in args.input:
        if not os.path.exists(f):
            print("%s dose not exsit." % f)
            sys.exit(1)

    if os.path.exists(args.output):
        print("output file already exsits.")
        sys.exit(1)

def f1(p,r):
    if p+r==0:
        return 0
    else:
        return 2*p*r/(p+r)

def main():

    process_options()
    colors = ['#1f77b4','#2ca02c','#9467bd','#8c564b','#ff7f0e','blue','red']

    df_list = []

    for f in args.input:
        cur_df = pandas.read_csv(f)
        cur_df['f1'] = cur_df.apply(lambda x: f1(x['precision'],x['recall']), axis=1)
        cur_fmax = cur_df['f1'].max()
        cur_max_point = cur_df[cur_df['f1'] == cur_fmax].values[0][0:2]
        df_list.append({
            'name': os.path.basename(f).split('.')[0],
            'points': cur_df[[0,1]].values,
            'fmax': cur_fmax,
            'max_point': cur_max_point
        })

    fig = plt.figure(figsize=(11,8))
    title = fig.suptitle(args.title, fontsize=30)
    ax = fig.add_subplot(111)
    ax.axis([0, 1, 0, 1])
    ax.axes.tick_params(labelsize=16)
    ax.set_xlabel('Recall', fontsize=18)
    ax.set_ylabel('Precision', fontsize=18)

    lines = []

    # F1 curve
    for f_score in np.arange(0.1,1,0.1):
        x = np.linspace(0.01, 1)
        y = f_score * x / (2 * x - f_score)
        l, = ax.plot(x[y >= 0], y[y >= 0], color='#7f8c8d', alpha=0.2)
        ax.annotate('f1={0:0.1f}'.format(f_score), xy=(0.9, y[45] + 0.02))

    for ind, df in enumerate(df_list):
        line = df['points']
        X = [ p[0] for p in line]
        Y = [ p[1] for p in line]

        # Draw line
        if df['name'] == 'Naive' or df['name'] == 'BLAST':
            cur_line, = ax.plot(X, Y, c=colors[ind], label=df['name'], linestyle='--', linewidth=2.0)
        elif df['name'] == '1NN':
            cur_line, = ax.plot(df['max_point'][0], df['max_point'][1], c=colors[ind], label=df['name'], linewidth=2.0)
        else:
            cur_line, = ax.plot(X, Y, c=colors[ind], label=df['name'], linewidth=2.0)
        lines.append(cur_line)

        # Draw Fmax point
        ax.scatter( df['max_point'][0], df['max_point'][1], c=colors[ind], s=80)

    # draw legend
    leg = ax.legend(handler_map={ line:HandlerLine2D(numpoints=1) for line in lines}, loc='upper center',
     bbox_to_anchor=(0.5,-0.1), prop={'size':20}, ncol=2)

    fig.savefig(args.output, bbox_extra_artists=(leg,title,), bbox_inches='tight')
    fig.clf()


if __name__ == "__main__":
    start_time = time.time()
main()
print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
