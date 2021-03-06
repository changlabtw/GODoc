import os
import sys
import pandas
import time
import numpy as np
import argparse
from sklearn.decomposition import PCA
import multiprocessing
import pickle
from sklearn.externals import joblib

global args

def process_options():
    global args

    parser = argparse.ArgumentParser(description='PCA with nfold')
    parser.add_argument('-i','--vector_folder', help='Training vector folder')
    parser.add_argument('-l','--label_file', help='label file', default="")
    parser.add_argument('-list','--ID_list', action='store_true', help='swich label to ID list file')
    parser.add_argument('-a','--all_files', action='store_true', help='parse whole folder, without using label file')
    parser.add_argument('-m','--model_file',help='PCA model name', default="")
    parser.add_argument('-n','--n_components',help='PCA n_components', type=float, default=0.95)
    parser.add_argument('-w','--whiten', action='store_true')
    parser.add_argument('-o','--output_file',help='Output file name', default='pca_result.csv')
    parser.add_argument('-om','--output_model_file',help='Output PCA model name', default="pca_model.pkl")

    args = parser.parse_args()

    if not os.path.exists(args.vector_folder):
        print "vector_folder not found."
        sys.exit(1)

    if not os.path.exists(args.label_file) and args.all_files!=True:
        print "label_file not found."
        sys.exit(1)

    if not os.path.exists(args.model_file) and args.model_file != "":
        print "model_file not found."
        sys.exit(1)

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
        vector_sum = np.sum(cur_vector)
        if np.isnan(vector_sum) or vector_sum == 0:
            return None

    return [ID, cur_vector]

def load_vector_helper(args):
    return load_vector(*args)


def main():

    process_options()

    if args.all_files:
        file_name_list = [ f for f in os.listdir(args.vector_folder) if os.path.isfile(os.path.join(args.vector_folder, f))]
        ID_list = [ file_name.split('.')[0] for file_name in file_name_list]
    else:
        if args.ID_list:
            ID_df = pandas.read_csv(args.label_file, sep='\t', names=['ID'])
            ID_list = ID_df['ID'].unique()
        else:
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

    if ( args.model_file == "" ):
        if args.n_components == 1:
            pca_n_components = None
        else:
            pca_n_components = args.n_components
        if args.whiten:
            pca=PCA(n_components = pca_n_components, whiten=True)
        else:
            pca=PCA(n_components = pca_n_components)
        train_data = pca.fit_transform(train_data)
        pkl_pca = pickle.dumps(pca)
        joblib.dump(pkl_pca, args.output_model_file)
    else:
        pca = joblib.load(args.model_file)
        pca = pickle.loads(pca)
        train_data = pca.transform(train_data)

    with open(args.output_file,'w') as f:
        for ind, ID in enumerate(train_ID):
            f.write(ID)
            f.write(',')
            f.write(','.join(map(str,train_data[ind])))
            f.write('\n')

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
