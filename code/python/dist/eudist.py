import os
import sys
import pandas
import numpy
import time
import multiprocessing

global train_vec_file
global output_file
global train_vec_df

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
    global output_file

    knn_df = pandas.DataFrame(columns=["ID","dist"])
    test = train_vec_df.loc[ind,1:]
    for i in range(0,len(train_vec_df.index)):
        if i != ind:
            current_train = train_vec_df.loc[i,1:]
            dist = numpy.linalg.norm( test-current_train )
            if len(knn_df.index) < k:
                knn_df.loc[len(knn_df.index)] = [train_vec_df.loc[i,0],dist]
                knn_df = knn_df.sort_values(by = ["dist"]).reset_index(drop=True)
            elif dist < knn_df.loc[k-1,"dist"]:
                knn_df.loc[k-1] = [train_vec_df.loc[i,0], dist]
                knn_df = knn_df.sort_values(by = ["dist"]).reset_index(drop=True)

    knn_list = []
    for i in range(0,k):
        knn_list.append(knn_df.loc[i,'ID'] + ',' + str(knn_df.loc[i,'dist']))

    with open(output_file, 'a') as f:
        f.write(train_vec_df.loc[ind,0] + '\t' +'\t'.join(knn_list)+'\n')

    return knn_df

def knn_helper(args):
    return knn(*args)

def main():

    global train_vec_file
    global train_vec_df

    process_options()

    k = 10

    train_vec_df = pandas.read_csv(train_vec_file, sep='\t' ,header=None)

    pool = multiprocessing.Pool()
    knn_args = []

    for i in range(0,len(train_vec_df.index)):
        knn_args.append([i, k])

    p = multiprocessing.Pool()
    rs = p.map_async(knn_helper, knn_args)
    p.close() # No more work
    while (True):
      if (rs.ready()): break
      remaining = rs._number_left
      print "Waiting for", remaining, "tasks to complete..."
      time.sleep(2)

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
