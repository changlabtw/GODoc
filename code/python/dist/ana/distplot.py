import os
import sys
import pandas
import time
import multiprocessing
from sklearn.neighbors import BallTree
import matplotlib.pyplot as plt
import numpy as np
import math

global input_file
global input_df

def process_options(argv = sys.argv):
    global input_file
    global input_df

    if len(argv) < 2:
		print "Usage: %s input_file" % argv[0]
		sys.exit(1)
    elif len(argv) == 2:
        input_file = argv[1]

    if not os.path.exists(input_file):
        print "input_file not found."
        sys.exit(1)

def clean(ind,k):
    if k >= len(input_df.loc[ind]):
        k  = len(input_df.loc[ind])-1
    targets = input_df.loc[ind,1:k]
    return targets.apply(lambda x: float(x.split(',')[1])).describe()

def clean_helper(args):

    return clean(*args)

def main():

    global input_file
    global input_df

    process_options()

    input_df = pandas.read_csv(input_file, sep='\t' ,header=None)

    clean_args = []
    k = 10
    for i in range(0,len(input_df.index)):
        clean_args.append([i,k])

    pool = multiprocessing.Pool()
    p = multiprocessing.Pool()
    rs = p.map_async(clean_helper, clean_args)
    p.close() # No more work
    while (True):
      if (rs.ready()): break
      remaining = rs._number_left
      print "Waiting for", remaining, "tasks to complete..."
      time.sleep(2)

    results = rs.get()
    sta_df = pandas.DataFrame(columns=['mean','std','min','25%','50%','75%','max'])
    for i in range(0,len(results)):
        current = results[i]
        sta_df.loc[i] = [current['mean'],current['std'],current['min'],current['25%'],current['50%'],current['75%'],current['max']]

    data = []
    for i in range(0,len(sta_df.columns)):
        # print sta_df.columns[i]
        # print sta_df[sta_df.columns[i]].describe()
        if i > 1:
            data.append(sta_df[sta_df.columns[i]])

    # basic plot
    plt.figure().suptitle("%s k=%i" % (os.path.basename(input_file),k) )
    plt.boxplot(data, 0, '')
    plt.xticks([1, 2, 3, 4, 5], ['min','25%','50%','75%','max'])
    plt.savefig(input_file + ".png")
    plt.figure().suptitle("%s k=%i" % (os.path.basename(input_file),k) )
    plt.boxplot(data) #with outlineer
    plt.xticks([1, 2, 3, 4, 5], ['min','25%','50%','75%','max'])
    plt.savefig(input_file + "_with_outlineer.png")
    plt.figure().suptitle("%s k=%i" % (os.path.basename(input_file),k) )
    plt.boxplot(data[0]) #with outlineer
    plt.xticks([1], ['min'])
    plt.savefig(input_file + "_min_with_outlineer.png")
    plt.figure().suptitle("%s k=%i" % (os.path.basename(input_file),k) )
    plt.boxplot(data[0], 0, '')
    plt.xticks([1], ['min'])
    plt.savefig(input_file + "_min.png")


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
