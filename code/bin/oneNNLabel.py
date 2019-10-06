#!/usr/bin/env python
import os
import sys
import pandas
import time
import multiprocessing
import numpy
import math

global pred_res_file
global train_label_file
global test_label_file
global pred_res_df
global train_label_df
global test_label_df
global output_file

def process_options(argv = sys.argv):
    global pred_res_file
    global train_label_file
    global test_label_file
    global output_file

    if len(argv) < 5:
		print "Usage: %s pred_res_file train_label_file test_label_file output_file" % argv[0]
		sys.exit(1)
    elif len(argv) == 5:
        pred_res_file = argv[1]
        train_label_file = argv[2]
        test_label_file = argv[3]
        output_file = argv[4]

    if not os.path.exists(pred_res_file):
        print "pred_res_file not found."
        sys.exit(1)

    if not os.path.exists(train_label_file):
        print "train_label_file not found."
        sys.exit(1)

    if not os.path.exists(test_label_file):
        print "test_label_file not found."
        sys.exit(1)

def assign(ind):

    ID = pred_res_df.loc[ind,"ID"]
    org_class = test_label_df[ test_label_df['ID'] == ID ]['GO'].values
    if len(org_class) == 0:
        org_class = None
    else:
        org_class = ','.join(org_class)
    pred_ID = pred_res_df.loc[ind,"pred_ID"]
    if pred_ID == "NA":
        pred_class = []
    else:
        pred_class = train_label_df[ train_label_df['ID'] == pred_ID ]['GO'].values
    if len(pred_class) == 0:
        pred_class = None
    else:
        pred_class = ','.join(pred_class)

    return [ID, pred_ID, org_class, pred_class]

def assign_helper(args):
    return assign(*args)

def main():

    global pred_res_df
    global train_label_df
    global test_label_df

    process_options()

    pred_res_df = pandas.read_csv(pred_res_file, sep="\t", header=0)
    train_label_df = pandas.read_csv(train_label_file, sep="\t", names=["ID","GO"])
    test_label_df = pandas.read_csv(test_label_file, sep="\t", names=["ID","GO"])

    assign_args = []
    for ind in range(0,len(pred_res_df.index)):
        assign_args.append([ind])

    pool = multiprocessing.Pool()
    p = multiprocessing.Pool()
    rs = p.map_async(assign_helper, assign_args)
    p.close() # No more work
    while (True):
      if (rs.ready()): break
      remaining = rs._number_left
      print "Waiting for", remaining, "tasks to complete..."
      time.sleep(2)

    res_df = pandas.DataFrame(columns=["ID","pred_ID","org_class","pred_class"])
    results = rs.get()
    for i in range(0,len(results)):
        res_df.loc[i] = results[i]

    res_df.to_csv(output_file,sep='\t',index=False,na_rep='NA')

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
