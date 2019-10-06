#!/usr/bin/env python
import os
import sys
import pandas
import time
import multiprocessing
import numpy
import math
from goatools.obo_parser import GODag, GraphEngines
import argparse

global args
global pred_res_df
global godb

def process_options():
    global args

    parser = argparse.ArgumentParser(description='Get predict GO\'s parents of GO term.')
    parser.add_argument('-i', '--pred_res_file', help='CAFA2 format result')
    parser.add_argument('-o', '--output_file', help='Predict result in propagated', default='propagated_results.txt')
    parser.add_argument('-db','--database', help='Gene Ontology Database', default='go-basic.obo')

    args = parser.parse_args()

    if not os.path.exists(args.pred_res_file):
        print "pred_res_file not found."
        sys.exit(1)

    if not os.path.exists(args.database):
        print "database not found."
        sys.exit(1)

def find(ID):

    current_df = pred_res_df[pred_res_df['ID']==ID].reset_index(drop=True)
    propagated_df = pandas.DataFrame(columns=['GO','score'])

    for i in range(0,len(current_df.index)):
        current_leaf = current_df.loc[i,'GO']
        current_score = current_df.loc[i,'score']
        current_parents = list(godb.query_term(current_leaf).get_all_parents())
        current_list = [current_leaf] + current_parents
        new_rows = pandas.DataFrame({'ID':[ID] * len(current_list), 'GO':current_list, 'score':[current_score] * len(current_list) })
        propagated_df = propagated_df.append(new_rows)

    propagated_df = propagated_df.groupby("GO").max().reset_index()

    return [propagated_df['ID'].values, propagated_df['GO'].values, propagated_df['score'].values]

def find_helper(args):
    return find(*args)

def main():

    global pred_res_df
    global godb

    process_options()

    pred_res_df = pandas.read_csv(args.pred_res_file, sep="\t", names=['ID','GO','score'], engine='python', skiprows=3, skipfooter=1)

    godb = GODag(args.database)

    find_args = []
    for ID in pred_res_df['ID'].unique():
        find_args.append([ID])

    pool = multiprocessing.Pool()
    p = multiprocessing.Pool()
    rs = p.map_async(find_helper, find_args)
    p.close() # No more work
    while (True):
      if (rs.ready()): break
      remaining = rs._number_left
      print "Waiting for", remaining, "tasks to complete..."
      time.sleep(2)


    results = rs.get()
    with open(args.output_file, 'w') as f:
        f.write("AUTHOR TEAM_NAME\n")
        f.write("MODEL 1\n")
        f.write("KEYWORDS\tpropagate\n")
        for rows in results:
            for i in range(0,len(rows[0])):
                f.write(rows[0][i])
                f.write('\t')
                f.write(rows[1][i])
                f.write('\t')
                f.write(str(rows[2][i]))
                f.write('\n')
        f.write("END\n")

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
