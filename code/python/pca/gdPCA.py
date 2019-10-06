import os
import sys
import pandas
import time
import argparse
from sklearn.decomposition import PCA
import numpy as np

global args

def process_options(argv = sys.argv):
    global args

    parser = argparse.ArgumentParser(description='PCA')
    parser.add_argument('-train', '--train_vec_file', help='Training vector file')
    parser.add_argument('-test', '--test_vec_file', help='Testing vector file')
    parser.add_argument('-f','--format', help='Vector file format, c for csv and t for tsv', type=str, choices=['c','t'], default='c')
    parser.add_argument('-n','--num_fold',help='fold number', type=int, default=5)
    parser.add_argument('-o','--output_folder',help='Output file name', default='pca_result')

    args = parser.parse_args()

    if not os.path.exists(args.train_vec_file):
        print "train_vec_file not found."
        sys.exit(1)

    if not os.path.exists(args.test_vec_file):
        print "test_vec_file not found."
        sys.exit(1)

    if not os.path.exists(args.output_folder):
        os.mkdir(args.output_folder)

def main():

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

    # remove nan rows
    removeInd = []
    for i in range(0,len(train_vec_df.index)):
        if np.isnan(np.sum(train_vec_df.loc[i,1:])):
            removeInd.append(i)
            print "Skip %s row for train_vec, because of nan." % i
    train_vec_df = train_vec_df.drop(removeInd)
    removeInd = []
    for i in range(0,len(test_vec_df.index)):
        if np.isnan(np.sum(test_vec_df.loc[i,1:])):
            removeInd.append(i)
            print "Skip %s row of test_vec, because of nan." % i
    test_vec_df = test_vec_df.drop(removeInd)

    train_ID = np.array(train_vec_df.loc[:,0])
    train_data = np.array(train_vec_df.loc[:,1:])
    test_ID = np.array(test_vec_df.loc[:,0])
    test_data = np.array(test_vec_df.loc[:,1:])

    pca = PCA(n_components = 0.95)
    train_x = pca.fit_transform(train_data)
    test_x = pca.transform(test_data)

    with open('%s/train_pca.csv' % args.output_folder,'w') as f:
        for ind, t in enumerate(train_ID):
            f.write(t)
            f.write(',')
            f.write(','.join(map(str,train_x[ind])))
            f.write('\n')
    with open('%s/test_pca.csv' % args.output_folder,'w') as f:
        for ind, t in enumerate(test_ID):
            f.write(t)
            f.write(',')
            f.write(','.join(map(str,test_x[ind])))
            f.write('\n')

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
