import os
import sys
import pandas
import time
import numpy as np
import argparse
from sklearn.decomposition import PCA
import pickle
from sklearn.externals import joblib

global args

def process_options():
    global args

    parser = argparse.ArgumentParser(description='PCA with nfold')
    parser.add_argument('-i','--vector_file', help='Training vector folder')
    parser.add_argument('-o','--output_file',help='Output file name', default='pca_result.csv')
    parser.add_argument('-m','--model_file',help='Output model name', default='pca_model.pkl')

    args = parser.parse_args()

    if not os.path.exists(args.vector_file):
        print "vector_folder not found."
        sys.exit(1)

def main():

    process_options()

    with open(args.vector_file, 'r') as f:
        lines = f.read().splitlines()

    train_ID = []
    train_data = []
    for line in lines:
        curent_vector = filter(bool, line.split(','))
        train_ID.append(curent_vector[0])
        train_data.append(map(float,curent_vector[1:]))

    train_ID = np.array(train_ID)
    train_data = np.array(train_data)

    pca=PCA(n_components = 0.95)
    train_data = pca.fit_transform(train_data)

    pkl_pca = pickle.dumps(pca)
    joblib.dump(pca, args.model_file)

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
