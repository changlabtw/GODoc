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

    parser = argparse.ArgumentParser(description='Get preddict GO\'s parents of GO term.')
    parser.add_argument('-i', '--pred_res_file', help='Training vector file')
    parser.add_argument('-o', '--output_file', help='Testing vector file')
    parser.add_argument('-db','--database', help='Vector file format, c for csv and t for tsv')

    args = parser.parse_args()

    if not os.path.exists(args.pred_res_file):
        print "pred_res_file not found."
        sys.exit(1)

    if not os.path.exists(args.database):
        print "database not found."
        sys.exit(1)

def find(ind):

    pred_class = set()

    for go in pred_res_df.loc[ind,"pred_class"].split(','):
        current_parents = godb.query_term(go).get_all_parents()
        pred_class = pred_class | current_parents

    return [ind, ','.join(pred_class)]

def find_helper(args):
    return find(*args)

def main():

    global pred_res_df
    global godb

    process_options()

    pred_res_df = pandas.read_csv(args.pred_res_file, sep="\t", header=0)

    godb = GODag(args.database)

    find_args = []
    for ind in pred_res_df.index[-pred_res_df['pred_ID'].isnull()]:
        find_args.append([ind])

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
    for i in range(0,len(results)):
        pred_res_df.loc[results[i][0],'pred_class'] = results[i][1]

    pred_res_df.to_csv(args.output_file,sep='\t',index=False,na_rep='NA')

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
