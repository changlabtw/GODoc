import os
import sys
import pandas
import time
import multiprocessing
import numpy
import argparse

global pred_res_df
global train_label_df
global args

def process_options(argv = sys.argv):
    global args

    parser = argparse.ArgumentParser(description='Get CAFA format from 1nn predict result')
    parser.add_argument('-i', '--pred_res_file', help='1nn predict result file')
    parser.add_argument('-l', '--train_label_file', help='Training label file')
    parser.add_argument('-o','--output_file',help='Output file name', default='leaf_score.txt')

    args = parser.parse_args()

    if not os.path.exists(args.pred_res_file):
        print "pred_res_file not found."
        sys.exit(1)

    if not os.path.exists(args.train_label_file):
        print "train_label_file not found."
        sys.exit(1)


def assign(ind):

    ID = pred_res_df.loc[ind,"ID"]
    pred_ID = pred_res_df.loc[ind,"pred_ID"]
    if pred_ID == "NA":
        pred_class = []
    else:
        pred_class = pandas.Series(train_label_df.loc[pred_ID]['GO']).values

    return [ID, pred_class]

def assign_helper(args):
    return assign(*args)

def main():

    global pred_res_df
    global train_label_df
    global test_label_df

    process_options()

    pred_res_df = pandas.read_csv(args.pred_res_file, sep="\t", header=0)
    train_label_df = pandas.read_csv(args.train_label_file, sep="\t", names=["ID","GO"])
    train_label_df = train_label_df.set_index(['ID'])

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


    with open(args.output_file, 'w') as f:
        f.write("AUTHOR NCCUCS\n")
        f.write("MODEL 1\n")
        f.write("KEYWORDS\t1NN\n")
        results = rs.get()
        for row in results:
            cur_ID = row[0]
            cur_gos = row[1]
            for go in cur_gos:
                f.write(cur_ID)
                f.write('\t')
                f.write(go)
                f.write('\t')
                f.write('1.00')
                f.write('\n')
        f.write('END')

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
