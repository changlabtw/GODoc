import os
import sys
import pandas
import time
import multiprocessing
import matplotlib.pyplot as plt
import argparse

global args
global knn_df

def process_options():
    global args

    parser = argparse.ArgumentParser(description='Plot KNN distribution')
    parser.add_argument('-i', '--knn_file', help='KNN file')
    parser.add_argument('-k', '--k', help='k number to ana, default: all', type=int, default=0)
    parser.add_argument('-o','--output_folder',help='Output folder name', default='knn_plot')

    args = parser.parse_args()

    if not os.path.exists(args.knn_file):
        print "knn_file not found."
        sys.exit(1)

    if not os.path.exists(args.output_folder):
        os.mkdir(args.output_folder)

def clean(ind,k):

    targets = knn_df.loc[ind,'pred_ID'].split(';')
    dist = []
    if k <= len(targets) and k != 0:
        targets = targets[0:k]
    for t in targets:
        cur_dist = float(t.split(',')[1])
        if cur_dist == 0:
            continue
        else:
            dist.append(cur_dist)

    return pandas.Series(dist).describe()

def clean_helper(args):

    return clean(*args)

def main():

    global knn_df

    process_options()

    knn_df = pandas.read_csv(args.knn_file, sep='\t', header=0)

    clean_args = []
    for i in range(0,len(knn_df.index)):
    # for i in range(0,1):
        clean_args.append([i,args.k])

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
    plt.figure().suptitle("%s k=%i" % (os.path.basename(args.knn_file),args.k) )
    plt.boxplot(data, 0, '')
    plt.xticks([1, 2, 3, 4, 5], ['min','25%','50%','75%','max'])
    plt.savefig(args.output_folder + '/' + args.knn_file + ".png")
    plt.figure().suptitle("%s k=%i" % (os.path.basename(args.knn_file),args.k) )
    plt.boxplot(data) #with outlineer
    plt.xticks([1, 2, 3, 4, 5], ['min','25%','50%','75%','max'])
    plt.savefig(args.output_folder + '/' + args.knn_file + "_with_outlineer.png")
    plt.figure().suptitle("%s k=%i" % (os.path.basename(args.knn_file),args.k) )
    plt.boxplot(data[0]) #with outlineer
    plt.xticks([1], ['min'])
    plt.savefig(args.output_folder + '/' + args.knn_file + "_min_with_outlineer.png")
    plt.figure().suptitle("%s k=%i" % (os.path.basename(args.knn_file),args.k) )
    plt.boxplot(data[0], 0, '')
    plt.xticks([1], ['min'])
    plt.savefig(args.output_folder + '/' + args.knn_file + "_min.png")


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
