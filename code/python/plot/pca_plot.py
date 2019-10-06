import os
import re
import sys
import time
import glob
import pandas
import argparse
import matplotlib.pyplot as plt
import numpy as np
import json

def process_options():
    global args

    parser = argparse.ArgumentParser(description='Plot cumulative of pixel difference count')
    parser.add_argument('-i', '--input', type=str, required=True, help='Data')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output')

    args = parser.parse_args()

    if not os.path.exists(args.input)::
        print("input file does not exsit.")
        sys.exit(1)

    if os.path.exists(args.output):
        print("output file already exsits.")
        sys.exit(1)

def fromjson(fname):
    with open(fname) as f:
        return json.load(f)

def main():

    process_options()
    colors = ['#1f77b4','#ff7f0e','#2ca02c','#9467bd','#8c564b','#e377c2','#7f7f7f','#bcbd22','#17becf']

    data = fromjson(args.input)

    fig = plt.figure(figsize=(11,8))
    fig.suptitle(data['title'], fontsize=30)
    ax = fig.add_subplot(111)
    ax.axis([data['X'][1], data['X'][2], data['Y'][1], data['Y'][2]])
    ax.axes.tick_params(labelsize=16)
    ax.set_xlabel(data['X'][0], fontsize=18)
    ax.set_ylabel(data['Y'][0], fontsize=18)

    lines = []

    x = np.arange(data['X'][1], data['X'][2],0.005)

    for ind, line in enumerate(data['lines']):
        cur_line, = ax.plot(x, line['points'], c=colors[ind], label=line['name'])
        lines.append(cur_line)




if __name__ == "__main__":
    start_time = time.time()
main()
print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
