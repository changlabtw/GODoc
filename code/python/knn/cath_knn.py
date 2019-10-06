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
global tree
global args

def process_options():
    global args

    parser = argparse.ArgumentParser(description='KNN for tsv or csv vector files.')
    parser.add_argument('-train', '--train_vec_file', help='Training vector file')
    parser.add_argument('-test', '--test_vec_file', help='Testing vector file')
    parser.add_argument('-train_m', '--train_map_file', help='Training CATH map file')
    parser.add_argument('-test_m', '--test_map_file', help='Testing CATH map file')
    parser.add_argument('-f','--format', help='Vector file format, c for csv and t for tsv', type=str, choices=['c','t'], default='c')
    parser.add_argument('-map','--map_format', help='Vector file format, c for csv and t for tsv', type=str)
    parser.add_argument('-k','--k',help='KNN number', type=int, default=1)
    parser.add_argument('-t','--type',help='CATH filter', type=str, choices=['sf','ff','ml'], default='ff')
    parser.add_argument('-nd','--disable_distance',help='Output without distance', action='store_true')
    parser.add_argument('-o','--output',help='Output file name', default='pred_res.tsv')

    args = parser.parse_args()

    if not os.path.exists(args.train_vec_file):
        print "train_vec_file not found."
        sys.exit(1)

    if not os.path.exists(args.test_vec_file):
        print "test_vec_file not found."
        sys.exit(1)

    if not os.path.exists(args.train_map_file):
        print "train_map_file not found."
        sys.exit(1)

    if not os.path.exists(args.test_map_file):
        print "test_map_file not found."
        sys.exit(1)

    if os.path.exists(args.output):
        print "output allready exists."
        sys.exit(1)

def cath_knn(cath, target_IDs, k = 1):

    x_test = test_vec_df[test_vec_df[0].isin(target_IDs)].iloc[:,1:-3].values

    if cath == None:
        x_train = train_vec_df.iloc[:,1:-3].values
        train_IDs = train_vec_df.iloc[:,0].values
        tree = BallTree(x_train)
    else:
        x_train = train_vec_df[train_vec_df[args.type] == cath].iloc[:,1:-3].values
        train_IDs = train_vec_df[train_vec_df[args.type] == cath].iloc[:,0].values
        tree = BallTree(x_train)

    if k > len(x_train):
        k = len(x_train)
    distances, indices = tree.query(x_test, k=k)

    res = []

    for ind, target in enumerate(target_IDs):
        if args.disable_distance:
            res.append([target, ';'.join(train_IDs[indices[ind]]) ])
        else:
            pred_pairs = ';'.join([','.join([x[0],str(x[1])]) for x in zip(train_IDs[indices[ind]],distances[ind])])
            res.append([target, pred_pairs ])

    return res

def cath_knn_helper(args):
    return cath_knn(*args)

def main():

    global train_vec_df
    global test_vec_df

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

    useless_trainID = []
    for i in range(0,len(train_vec_df)):
        if np.isnan(np.sum(train_vec_df.iloc[i,1:-3])):
            useless_trainID.append(train_vec_df.iloc[i,0])
            print "Skip %s row for train_vec, because of nan." % i
    train_vec_df = train_vec_df[~train_vec_df[0].isin(useless_trainID)]

    unpred_ID = []
    for i in range(0,len(test_vec_df)):
        if np.isnan(np.sum(test_vec_df.iloc[i,1:-3])):
            unpred_ID.append(test_vec_df.iloc[i,0])
            print "Skip %s of test_vec, because of nan." % test_vec_df.iloc[i,0]
    test_vec_df = test_vec_df[~test_vec_df[0].isin(unpred_ID)]


    if args.map_format != None:
        train_map_df = pandas.read_csv(args.train_map_file, sep='\t', names=[0,'sf','ff','ml'], skiprows=1)
        test_map_df = pandas.read_csv(args.test_map_file, sep='\t', names=[0,'sf','ff','ml'], skiprows=1)
    else:
        train_map_df = pandas.read_csv(args.train_map_file, sep='\t', names=[0,args.map_format], skiprows=1)
        test_map_df = pandas.read_csv(args.test_map_file, sep='\t', names=[0,args.map_format], skiprows=1)

    train_vec_df = pandas.merge(train_vec_df, train_map_df, on=0, how='left')
    test_vec_df = pandas.merge(test_vec_df, test_map_df, on=0, how='left')

    cover_list = np.intersect1d(train_vec_df[args.type].unique(), test_vec_df[args.type].unique())
    cover_list = [ x for x in cover_list if pandas.notnull(x) ] #remove nan
    cover_ID = test_vec_df[test_vec_df[args.type].apply(lambda x:  x in cover_list)][0].values
    print "%i of test protein use CATH-KNN, %i of test protein use 1NN." % (len(cover_ID), len(test_vec_df) - len(cover_ID))

    cath_knn_args = []
    uncover_ID = test_vec_df[ (test_vec_df[args.type].isnull()) | ~(test_vec_df[args.type].isin(cover_list))][0].values
    if len(uncover_ID) != 0:
        cath_knn_args.append([None, uncover_ID, args.k])
    for cur_cath in cover_list:
        cur_targets = test_vec_df[test_vec_df[args.type] == cur_cath][0].values
        cath_knn_args.append([cur_cath, cur_targets, args.k])

    pool = multiprocessing.Pool()
    p = multiprocessing.Pool()
    rs = p.map_async(cath_knn_helper, cath_knn_args)
    p.close() # No more work
    while (True):
      if (rs.ready()): break
      remaining = rs._number_left
      print "Waiting for", remaining, "tasks to complete..."
      time.sleep(2)

    results = rs.get()
    with open(args.output, 'w') as f:
        f.write('ID\tpred_ID\n')
        for rows in results:
            for row in rows:
                f.write(row[0])
                f.write('\t')
                f.write(row[1])
                f.write('\n')
        if len(unpred_ID) != 0:
            for ID in unpred_ID:
                f.write(ID)
                f.write('\t')
                f.write('NA')
                f.write('\n')

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
