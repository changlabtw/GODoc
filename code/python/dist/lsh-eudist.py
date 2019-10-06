import os
import sys
import pandas
import time
import multiprocessing
from sklearn.neighbors import LSHForest

global train_vec_file
global output_file
global train_vec_df
global lshf

def process_options(argv = sys.argv):
    global train_vec_file
    global output_file

    if len(argv) < 3:
		print "Usage: %s train_vec_file output_file" % argv[0]
		sys.exit(1)
    elif len(argv) == 3:
        train_vec_file = argv[1]
        output_file = argv[2]

    if not os.path.exists(train_vec_file):
        print "train_vec_file not found."
        sys.exit(1)

def knn(ind, k = 3):
    global train_vec_df

    test = train_vec_df.loc[ind,1:]
    test = test.reshape(1,-1)
    distances, indices = lshf.kneighbors(test, n_neighbors=k)

    knn_list = []
    for i in range(1,k):
        knn_list.append(train_vec_df.loc[indices[0][i],0] + ',' + str(float(distances[0][i])))

    return train_vec_df.loc[ind,0] + '\t' +'\t'.join(knn_list)+'\n'

def knn_helper(args):
    return knn(*args)

def main():

    global train_vec_file
    global train_vec_df
    global lshf

    process_options()

    k = 1001

    train_vec_df = pandas.read_csv(train_vec_file, sep='\t' ,header=None)

    x_train = []
    knn_args = []
    for i in range(0,len(train_vec_df.index)):
        x_train.append(train_vec_df.ix[i][1:])
        knn_args.append([i, k])

    lshf = LSHForest()
    lshf.fit(x_train)

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
    with open(output_file, 'w') as f:
        f.writelines(results)

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
