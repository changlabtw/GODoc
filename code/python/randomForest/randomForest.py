from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
import numpy as np
import pandas
import argparse
import time
import sys
import os
import multiprocessing

global args
global train_label_df
global train_vec_df

def process_options(argv = sys.argv):
    global args

    parser = argparse.ArgumentParser(description='Random Forest.')
    parser.add_argument('-train_vec', '--train_vec_file', help='')
    parser.add_argument('-test_vec', '--test_vec_file', help='')
    parser.add_argument('-train_label', '--train_label_file', help='')
    parser.add_argument('-f','--format', help='Vector file format, c for csv and t for tsv', type=str, choices=['c','t'], default='c')
    parser.add_argument('-o','--output_file',help='Output file name', default='result.tsv')

    args = parser.parse_args()

    if not os.path.exists(args.train_vec_file):
        print "train_vec_file not found."
        sys.exit(1)

    if not os.path.exists(args.train_label_file):
        print "train_label_file not found."
        sys.exit(1)

    if not os.path.exists(args.train_vec_file):
        print "test_vec_file not found."
        sys.exit(1)

def build(ind):

    if np.isnan(np.sum(train_vec_df.loc[ind,1:])):
        print "Skip %s row for train_vec, because of nan." % i
        return None
    else:
        current_ID = train_vec_df.loc[ind,0]
        current_gos = train_label_df[ train_label_df['ID'] == current_ID ]['GO'].values.tolist()
        if len(current_gos) == 0:
            return None
        else:
            current_x = list(train_vec_df.loc[ind,1:])
            current_y = current_gos
            return [current_x, current_y]

def build_helper(args):
    return build(*args)

def main():

    global train_label_df
    global train_vec_df
    global train_x
    global train_y

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

    train_vec_df = pandas.read_csv(args.train_vec_file, header=None, sep='\t')
    train_label_df = pandas.read_csv(args.train_label_file, names=['ID','GO'], sep='\t')
    test_vec_df = pandas.read_csv(args.test_vec_file, header=None, sep='\t')

    labels_sta = train_label_df.groupby('GO').count().reset_index()
    target_labels = labels_sta[labels_sta['ID']>=150]['GO'].values
    train_label_df = train_label_df[train_label_df['GO'].isin(target_labels)]

    pool = multiprocessing.Pool()
    build_args = []

    for i in range(0,len(train_vec_df.index)):
        build_args.append([i])

    p = multiprocessing.Pool()
    rs = p.map_async(build_helper, build_args)
    p.close() # No more work
    while (True):
      if (rs.ready()): break
      remaining = rs._number_left
      print "Waiting for", remaining, "tasks to complete..."
      time.sleep(2)

    train_x = []
    train_y = []
    results = rs.get()
    for row in results:
        if row != None:
            train_x.append(row[0])
            train_y.append(row[1])

    train_y_mul = MultiLabelBinarizer()
    train_y = train_y_mul.fit_transform(train_y)
    labes = train_y_mul.classes_

    print "Finished load trining data"

    test_x = []
    test_ID = []
    unpred_ID = []
    for i in range(0,len(test_vec_df.index)):
        if np.isnan(np.sum(test_vec_df.loc[i,1:])):
            unpred_ID.append(test_vec_df.loc[i,0])
            print "Skip %s of test_vec, because of nan." % test_vec_df.loc[i,0]
        else:
            test_ID.append(test_vec_df.loc[i,0])
            test_x.append(list(test_vec_df.loc[i,1:]))

    print "Finished load testing data"

    rf = RandomForestClassifier(n_estimators=10,max_features=36,n_jobs=8)
    rf.fit(train_x, train_y)
    res = rf.predict(test_x)
    with open(args.output_file,'w') as f:
        f.write('ID\tpred_class\n')
        for ind, r in enumerate(res):
            f.write(test_ID[ind])
            f.write('\t')
            f.write(','.join(labes[ list( ind for ind, l in enumerate(r) if l == 1) ]))
            f.write('\n')
        for u in unpred_ID:
            f.write(u)
            f.write('\t')
            f.write('\n')

if __name__=="__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
