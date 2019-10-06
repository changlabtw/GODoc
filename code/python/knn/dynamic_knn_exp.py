import os
import sys
import pandas
import time
import multiprocessing
from sklearn.neighbors import BallTree
import numpy as np
import argparse

global train_vec_df
global test_vec_df
global base_vec_df
global tree
global args

def process_options():
    global args

    parser = argparse.ArgumentParser(description='Dynamic KNN Experiment')
    parser.add_argument('-b', '--base_knn_file', help='Training 1NN result')
    parser.add_argument('-train', '--train_vec_file', help='Training vector file')
    parser.add_argument('-test', '--test_vec_file', help='Testing vector file')
    parser.add_argument('-f','--format', help='Vector file format, c for csv and t for tsv', type=str, choices=['c','t'], default='c')
    parser.add_argument('-o','--output',help='Output file name', default='pred_res.tsv')

    args = parser.parse_args()

    if not os.path.exists(args.base_knn_file):
        print "base_knn_file not found."
        sys.exit(1)

    if not os.path.exists(args.train_vec_file):
        print "train_vec_file not found."
        sys.exit(1)

    if not os.path.exists(args.test_vec_file):
        print "test_vec_file not found."
        sys.exit(1)

    if os.path.exists(args.output):
        print "output allready exists."
        sys.exit(1)

def knn(ind, threshold):

    test = test_vec_df.loc[ind,1:]
    test = test.reshape(1,-1)

    indices, distances = tree.query_radius(test, r=threshold, return_distance=True, sort_results=True)

    zero_ind = [ index for index, val in enumerate(distances[0]) if val == 0 ]
    if len(zero_ind)!=0:
        distances = [[ val for index,val in enumerate(distances[0]) if not(index in zero_ind)]]
        indices = [[ val for index,val in enumerate(indices[0]) if not(index in zero_ind)]]

    pred = []
    if len(indices[0]) == 0:
        return [None,None]
    for i in range(0,len(indices[0])):
        current_pair = train_vec_df.loc[indices[0][i],0] +','+ str(distances[0][i])
        pred.append(current_pair)
    return [test_vec_df.loc[ind,0],';'.join(pred)]

def knn_helper(args):
    return knn(*args)

def main():

    global train_vec_df
    global test_vec_df
    global tree

    process_options()

    if args.format == 'c':
        train_vec_df = pandas.read_csv(args.train_vec_file, header=None)
        test_vec_df = pandas.read_csv(args.test_vec_file, header=None)
        # remove last column if it's empty
        if pandas.isnull(train_vec_df.loc[0,len(train_vec_df.columns)-1]):
            train_vec_df = train_vec_df.drop(len(train_vec_df.columns)-1, axis = 1)
        if pandas.isnull(test_vec_df.loc[0,len(test_vec_df.columns)-1]):
            test_vec_df = test_vec_df.drop(len(test_vec_df.columns)-1, axis = 1)
    elif args.format == 't':
        train_vec_df = pandas.read_csv(args.train_vec_file, sep='\t' ,header=None)
        test_vec_df = pandas.read_csv(args.test_vec_file, sep='\t' ,header=None)


    #Find distance threshold
    base_knn_df = pandas.read_csv(args.base_knn_file, sep='\t' ,header=0)
    base_knn_df['dist'] = base_knn_df['pred_ID'].apply(lambda x: float(x.split(';')[0].split(',')[1]))

    threshold = base_knn_df['dist'].describe()['75%']

    #KNN
    x_train = []
    for i in range(0,len(train_vec_df.index)):
        if np.isnan(np.sum(train_vec_df.loc[i,1:])):
            print "Skip %s row for train_vec, because of nan." % i
        else:
            x_train.append(train_vec_df.ix[i][1:])

    tree = BallTree(x_train)

    knn_args = []
    unpred_ID = []
    for i in range(0,len(test_vec_df.index)):
        if np.isnan(np.sum(test_vec_df.loc[i,1:])):
            unpred_ID.append(test_vec_df.loc[i,0])
            print "Skip %s of test_vec, because of nan." % test_vec_df.loc[i,0]
        else:
            knn_args.append([i, threshold])

    pool = multiprocessing.Pool()
    p = multiprocessing.Pool()
    rs = p.map_async(knn_helper, knn_args)
    p.close() # No more work
    while (True):
      if (rs.ready()): break
      remaining = rs._number_left
      print "Waiting for", remaining, "tasks to complete..."
      time.sleep(2)

    results = rs.get()
    pred_res_df = pandas.DataFrame(columns=["ID","pred_ID"])
    for i in range(0,len(results)):
        if results[i][0] is None:
            continue
        else:
            pred_res_df.loc[i] = results[i]
    if len(unpred_ID) != 0:
        newrows = pandas.DataFrame({"ID":unpred_ID,"pred_ID":[None]*len(unpred_ID)})
        pred_res_df = pred_res_df.append(newrows).reset_index(drop=True)
    pred_res_df.to_csv(args.output,sep='\t',index=False, na_rep='NA')

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
