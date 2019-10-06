#!/usr/bin/env python
import os
import sys
import pandas
import numpy
import time
import multiprocessing
import argparse

global args
global knn_df
global label_df

def process_options(argv = sys.argv):
    global args

    parser = argparse.ArgumentParser(description='KNN for tsv or csv vector files.')
    parser.add_argument('-i', '--knn_file', help='KNN output with distance file')
    parser.add_argument('-l', '--label_file', help='Training label file')
    parser.add_argument('-s','--score_formula', help='Score formula, 1: 1/dist, 2: log(1/dist), 3: sqrt(1/dist)', type=int, choices=[0,1,2], default=0)
    parser.add_argument('-o','--output_file',help='Output file name', default='vote_score.txt')

    args = parser.parse_args()

    if not os.path.exists(args.knn_file):
        print "knn_file not found."
        sys.exit(1)

    if not os.path.exists(args.label_file):
        print "label_file not found."
        sys.exit(1)

def vote(ind, score_formula):

    global knn_df
    global label_df

    dist_pairs = knn_df.loc[ind,'pred_ID'].split(";")
    dist_df = pandas.DataFrame(columns=["ID","dist"])
    for i, pair in enumerate(dist_pairs):
        dist_df.loc[i] = [pair.split(',')[0], float(pair.split(',')[1])]

    gos = pandas.DataFrame(columns=["GO","score"])

    for j in range(0,len(dist_df.index)):
        if dist_df.loc[j,"dist"] == 0.0:
            # skip if 1NN is itself
            continue
        current_gos = label_df[label_df["ID"] == dist_df.loc[j,"ID"]]["GO"].values

        if score_formula == 0:
            # score = 1/dist
            current_score = [1.0/dist_df.loc[j,"dist"]]
            new_rows = pandas.DataFrame({"GO":current_gos, "score": current_score*len(current_gos)})
        elif score_formula == 1:
            # score = log(1/dist)
            current_score = [numpy.log(1.0/dist_df.loc[j,"dist"])]
            new_rows = pandas.DataFrame({"GO":current_gos, "score": current_score*len(current_gos)})
        elif score_formula == 2:
            # score = sqrt(1/dist)
            current_score = [numpy.sqrt(1.0/dist_df.loc[j,"dist"])]
            new_rows = pandas.DataFrame({"GO":current_gos, "score": current_score*len(current_gos)})
        gos = gos.append(new_rows)

    gos_sta = gos.groupby("GO").sum().sort_values(by=["score"], ascending=False).reset_index()


    gos_sta['map_score'] = gos_sta['score']/gos_sta['score'].max()
    ID = knn_df.loc[ind,'ID']

    score_list = []
    for k in range(0,len(gos_sta.index)):
        score_list.append( ID + '\t' + gos_sta.loc[k,'GO'] + '\t' + format(round(gos_sta.loc[k,'map_score'],2),'.2f') + '\n' )

    return score_list

def vote_helper(args):
    return vote(*args)

def main():

    global knn_df
    global label_df
    method = ['1/dist','log(1/dist)','sqrt(1/dist)']

    process_options()

    knn_df = pandas.read_csv(args.knn_file, sep='\t' ,header=0)
    label_df = pandas.read_csv(args.label_file, sep='\t' ,names=["ID","GO"])

    print "Unpred protein amount: %i" % len(knn_df[knn_df['pred_ID'].isnull()].index)
    knn_df = knn_df[-knn_df['pred_ID'].isnull()].reset_index(drop=True) #drop unpred protein

    pool = multiprocessing.Pool()
    vote_args = []

    for i in range(0,len(knn_df.index)):
    # for i in range(1,2):
        vote_args.append([i, args.score_formula])

    p = multiprocessing.Pool()
    rs = p.map_async(vote_helper, vote_args)
    p.close() # No more work
    while (True):
      if (rs.ready()): break
      remaining = rs._number_left
      print "Waiting for", remaining, "tasks to complete..."
      time.sleep(2)

    with open(args.output_file, 'w') as f:
        f.write("AUTHOR TEAM_NAME\n")
        f.write("MODEL 1\n")
        f.write("KEYWORDS\t"+method[args.score_formula]+"\n")
        results = rs.get()
        for str_list in results:
            for line in str_list:
                f.write(line)
        f.write("END\n")

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
