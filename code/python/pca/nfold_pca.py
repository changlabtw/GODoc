import os
import sys
import pandas
import time
import numpy as np
import argparse
from sklearn.decomposition import PCA

global train_vec_df
global test_vec_df
global tree
global args

def process_options():
    global args

    parser = argparse.ArgumentParser(description='PCA with nfold')
    parser.add_argument('-t', '--train_vec_file', help='Training vector file')
    parser.add_argument('-f','--format', help='Vector file format, c for csv and t for tsv', type=str, choices=['c','t'], default='c')
    parser.add_argument('-n','--num_fold',help='fold number', type=int, default=5)
    parser.add_argument('-o','--output_folder',help='Output file name', default='nfold_result')

    args = parser.parse_args()

    if not os.path.exists(args.train_vec_file):
        print "train_vec_file not found."
        sys.exit(1)

    if not os.path.exists(args.output_folder):
        os.mkdir(args.output_folder)

def main():

    process_options()

    # if args.format == 'c':
    #     train_vec_df = pandas.read_csv(args.train_vec_file, header=None)
    #     # remove last column if it's empty
    #     if pandas.isnull(train_vec_df.loc[0,len(train_vec_df.columns)-1]):
    #         train_vec_df = train_vec_df.drop(len(train_vec_df.columns)-1, axis = 1)
    # elif args.format == 't':
    #     train_vec_df = pandas.read_csv(args.train_vec_file, sep='\t' ,header=None)

    train_ID = []
    train_data = []

    with open(args.train_vec_file, 'r') as f:
        for line in f:
            cur_list = []
            if args.format == 'c':
                cur_list = line.split(',')
            elif args.format == 't':
                cur_list = line.split('\t')
            train_ID.append(cur_list[0])
            if (cur_list[-1] == '\n'):
                train_data.append(map(float,(cur_list[1:-1])))
            else:
                train_data.append(map(float,(cur_list[1:])))

    # # remove nan rows
    # removeInd = []
    # for i in range(0,len(train_vec_df.index)):
    #     if np.isnan(np.sum(train_vec_df.loc[i,1:])):
    #         removeInd.append(i)
    #         print "Skip %s row for train_vec, because of nan." % i
    # train_vec_df = train_vec_df.drop(removeInd)

    removeInd = []
    for i in range(0,len(train_data)):
        if np.isnan(np.sum(train_data[i])):
            removeInd.append(i)

    train_ID = np.delete(train_ID, removeInd)
    train_data = np.delete(train_data, removeInd, axis=0)

    # train_ID = np.array(train_vec_df.loc[:,0])
    # train_data = np.array(train_vec_df.loc[:,1:])


    num_fold = args.num_fold
    for fold in range(0,num_fold):
        train_i = []
        test_i = []
        for i in range(0,len(train_ID)):
            if i % num_fold != fold:
                train_i.append(i)
            else:
                test_i.append(i)
        train_x = train_data[train_i]
        test_x = train_data[test_i]

        pca=PCA(n_components = 0.95)
        train_x = pca.fit_transform(train_x)
        test_x = pca.transform(test_x)

        cur_output = ("%s/fold%i" % (args.output_folder, fold))
        if not os.path.exists(cur_output):
            os.mkdir(cur_output)
        with open('%s/train_pca.csv' % cur_output,'w') as f:
            for ind, t in enumerate(train_i):
                f.write(train_ID[t])
                f.write(',')
                f.write(','.join(map(str,train_x[ind])))
                f.write('\n')
        with open('%s/test_pca.csv' % cur_output,'w') as f:
            for ind, t in enumerate(test_i):
                f.write(train_ID[t])
                f.write(',')
                f.write(','.join(map(str,test_x[ind])))
                f.write('\n')

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
