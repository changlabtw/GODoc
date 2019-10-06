import os
import sys
import pandas
import time
import multiprocessing
import matplotlib.pyplot as plt
import argparse
import re

global args
global lines

def process_options():
    global args

    parser = argparse.ArgumentParser(description='Plot KNN distribution')
    parser.add_argument('-i', '--knn_file', help='KNN file')
    parser.add_argument('-o','--output_folder',help='Output folder name', default='knn_plot')

    args = parser.parse_args()

    if not os.path.exists(args.knn_file):
        print "knn_file not found."
        sys.exit(1)

    if not os.path.exists(args.output_folder):
        os.mkdir(args.output_folder)

def clean(ind):

    targets = re.split('/t|;',lines[ind])[1:]
    dist = []
    for t in targets:
        dist.append(float(t.split(',')[1]))

    return pandas.Series(dist).describe()

def clean_helper(args):

    return clean(*args)

def main():

    global lines

    process_options()

    with open(args.knn_file, 'r') as f:
        lines = f.read().splitlines()


    clean_args = []
    for i in range(0,len(lines)):
        clean_args.append([i])

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

    sta_df = sta_df[-pandas.isnull(sta_df['mean'])]

    data = []
    for i in range(0,len(sta_df.columns)):
        if i > 1:
            data.append(sta_df[sta_df.columns[i]])

    # basic plot
    plt.figure().suptitle(os.path.basename(args.knn_file))
    plt.boxplot(data, 0, '')
    plt.xticks([1, 2, 3, 4, 5], ['min','25%','50%','75%','max'])
    plt.savefig(args.output_folder + '/' + os.path.basename(args.knn_file).split('.')[0] + ".png")
    plt.figure().suptitle(os.path.basename(args.knn_file) )
    plt.boxplot(data) #with outlineer
    plt.xticks([1, 2, 3, 4, 5], ['min','25%','50%','75%','max'])
    plt.savefig(args.output_folder + '/' + os.path.basename(args.knn_file).split('.')[0] + "_with_outlineer.png")


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
