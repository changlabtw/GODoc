import os
import sys
import pandas
import time
import multiprocessing
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier
import numpy as np

global train_vec_file
global test_vec_file

def process_options(argv = sys.argv):
    global train_vec_file
    global test_vec_file
    global output_file

    if len(argv) < 3:
		print "Usage: %s train_vec_file test_vec_file" % argv[0]
		sys.exit(1)
    elif len(argv) == 3:
        train_vec_file = argv[1]
        test_vec_file = argv[2]

    if not os.path.exists(train_vec_file):
        print "train_vec_file not found."
        sys.exit(1)

    if not os.path.exists(test_vec_file):
        print "test_vec_file not found."
        sys.exit(1)

def main():

    global train_vec_file
    global test_vec_file

    process_options()

    train_vec_df = pandas.read_csv(train_vec_file, header=None)
    test_vec_df = pandas.read_csv(test_vec_file, header=None)

    # remove last empty column
    train_vec_df = train_vec_df.loc[:,0:len(train_vec_df.columns)-2]
    test_vec_df = test_vec_df.loc[:,0:len(test_vec_df.columns)-2]

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

    train_data = np.array(train_vec_df.loc[:,1:])
    train_label = np.array(train_vec_df.loc[:,0])
    test_data = np.array(test_vec_df.loc[:,1:])
    test_label = np.array(test_vec_df.loc[:,0])

    t = time.time()
    pca=PCA(n_components = 0.95)
    train_x = pca.fit_transform(train_data)
    test_x = pca.transform(test_data)
    neighbors = KNeighborsClassifier(n_neighbors=1)
    neighbors.fit(train_x,train_label)
    pre= neighbors.predict(test_x)

    pred_res = pandas.DataFrame({'ID':test_label,'pred_ID':pre})

    pred_res.to_csv('pred_res', sep='\t', header=True, index=False)

    # train_pca.to_csv(os.path.basename(train_vec_file).split('.')[0]+'_pca.tsv',sep='\t',header=False,index=False)
    # test_pca.to_csv(os.path.basename(test_vec_file).split('.')[0]+'_pca.tsv',sep='\t',header=False,index=False)

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
