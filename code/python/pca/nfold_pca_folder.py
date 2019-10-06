import os
import sys
import pandas
import time
import numpy as np
import argparse
from sklearn.decomposition import PCA
import multiprocessing

global args

def process_options():
    global args

    parser = argparse.ArgumentParser(description='PCA with nfold')
    parser.add_argument('-i','--vector_folder', help='Training vector folder')
    parser.add_argument('-l','--label_file', help='label file')
    parser.add_argument('-n','--num_fold',help='fold number', type=int, default=5)
    parser.add_argument('-o','--output_folder',help='Output file name', default='nfold_result')

    args = parser.parse_args()

    if not os.path.exists(args.vector_folder):
        print "vector_folder not found."
        sys.exit(1)

    if not os.path.exists(args.label_file):
        print "label_file not found."
        sys.exit(1)

    if not os.path.exists(args.output_folder):
        os.mkdir(args.output_folder)

def load_vector(ID):

    cur_vector = []
    with open(args.vector_folder + ID + '.txt', 'r') as f:
        lines = f.read().splitlines()
        if len(lines) != 1:
            print "Skip " + ID + ".txt"
            return None
        else:
            cur_list = lines[0].split(',')
            if (cur_list[-1] == ''):
                cur_vector = map(float,(cur_list[:-1]))
            else:
                cur_vector = map(float,(cur_list))
        if np.isnan(np.sum(cur_vector)):
            return None

    return [ID, cur_vector]

def load_vector_helper(args):
    return load_vector(*args)


def main():

    process_options()

    label_df = pandas.read_csv(args.label_file, sep='\t', names=['ID', 'GO'])
    ID_list = label_df['ID'].unique()

    load_vector_args = []

    for ID in ID_list:
        if not os.path.exists(args.vector_folder + ID + '.txt'):
            print "Skip " + ID + ".txt"
        else:
            load_vector_args.append([ID])

    p = multiprocessing.Pool()
    rs = p.map_async(load_vector_helper, load_vector_args)
    p.close() # No more work
    while (True):
      if (rs.ready()): break
      remaining = rs._number_left
      print "Waiting for", remaining, "tasks to complete..."
      time.sleep(2)

    train_ID = []
    train_data = []

    results = rs.get()
    for row in results:
        if row == None:
            continue
        else:
            train_ID.append(row[0])
            train_data.append(row[1])

    del results
    del rs

    train_ID = np.array(train_ID)
    train_data = np.array(train_data)

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
