import os
import sys
import pandas
import time
import multiprocessing
import numpy

global pred_res_file
global train_label_file
global test_label_file
global output_file
global train_label_df
global test_label_df
global dist_df
global k

def process_options(argv = sys.argv):
    global pred_res_file
    global train_label_file
    global test_label_file
    global output_file
    global k

    if len(argv) < 5:
		print "Usage: %s pred_res_file train_label_file test_label_file output_file (k)" % argv[0]
		sys.exit(1)
    elif len(argv) == 5:
        pred_res_file = argv[1]
        train_label_file = argv[2]
        test_label_file = argv[3]
        output_file = argv[4]
        k = 0
    elif len(argv) == 6:
        pred_res_file = argv[1]
        train_label_file = argv[2]
        test_label_file = argv[3]
        output_file = argv[4]
        k = int(argv[5])

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

    global k

    ID = dist_df.loc[ind,0]
    org_class = test_label_df[ test_label_df['ID'] == ID ]['GO'].values
    res = "%s,%s" % (ID, ','.join(org_class))
    if k == 0:
        k = len(dist_df.loc[ind])
    for i in range(1,k):
        cur_id = dist_df.loc[ind,i].split(',')[0]
        cur_dist = dist_df.loc[ind,i].split(',')[1]
        cur_pred_class = train_label_df[ train_label_df['ID'] == cur_id ]['GO'].values
        res = "%s\t%s,%s,%s" % (res,cur_id,cur_dist,','.join(cur_pred_class))
    return res + "\n"

def assign_helper(args):
    return assign(*args)

def main():

    global train_label_df
    global test_label_df
    global dist_df

    process_options()

    dist_df = pandas.read_csv(pred_res_file, sep="\t", header=None)
    train_label_df = pandas.read_csv(train_label_file, sep="\t", names=["ID","GO"])
    test_label_df = pandas.read_csv(test_label_file, sep="\t", names=["ID","GO"])
    dist_df = dist_df[dist_df[0].isin(test_label_df['ID'].unique())].reset_index(drop=True)

    assign_args = []
    for i in range(0,len(dist_df.index)):
        assign_args.append([i])

    pool = multiprocessing.Pool()
    p = multiprocessing.Pool()
    rs = p.map_async(assign_helper, assign_args)
    p.close() # No more work
    while (True):
      if (rs.ready()): break
      remaining = rs._number_left
      print "Waiting for", remaining, "tasks to complete..."
      time.sleep(2)

    results = rs.get()
    with open(output_file, 'w') as f:
        for r in results:
            f.writelines(r)

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))