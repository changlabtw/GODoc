import os
import sys
import pandas
import numpy
import time
import multiprocessing

global train_vec_file
global test_vec_file
global train_label_file
global test_label_file
global output_file
global train_label_df
global test_label_df
global train_label_count

def process_options(argv = sys.argv):
    global train_vec_file
    global test_vec_file
    global train_label_file
    global test_label_file
    global output_file

    if len(argv) < 6:
		print "Usage: %s train_vec_file test_vec_file train_label_file test_label_file output_file" % argv[0]
		sys.exit(1)

    train_vec_file = argv[1]
    test_vec_file = argv[2]
    train_label_file = argv[3]
    test_label_file = argv[4]
    output_file = argv[5]

    if not os.path.exists(train_vec_file):
        print "train_vec_file not found."
        sys.exit(1)

    if not os.path.exists(test_vec_file):
        print "test_vec_file not found."
        sys.exit(1)

    if not os.path.exists(train_label_file):
        print "train_label_file not found."
        sys.exit(1)

    if not os.path.exists(test_label_file):
        print "test_label_file not found."
        sys.exit(1)

def knn(test_vec, train_vecs, k = 3):
    knn_df = pandas.DataFrame(columns=["ID","dist"])
    test = test_vec[1:]
    for i in range(0,len(train_vecs.index)):
        current_train = train_vecs.loc[i,1:]
        dist = numpy.linalg.norm( test-current_train )
        if len(knn_df.index) < k:
            knn_df.loc[len(knn_df.index)] = [train_vecs.loc[i,0],dist]
            knn_df = knn_df.sort_values(by = ["dist"]).reset_index(drop=True)
        elif dist < knn_df.loc[k-1,"dist"]:
            knn_df.loc[k-1] = [train_vecs.loc[i,0], dist]
            knn_df = knn_df.sort_values(by = ["dist"]).reset_index(drop=True)
    return knn_df

def knn_vote(test_vec, train_vecs, k):
    dist_df = knn(test_vec, train_vecs, k)
    gos = pandas.DataFrame(columns=["GO","score"])
    for j in range(0,len(dist_df.index)):
        current_gos = train_label_df[train_label_df["ID"] == dist_df.loc[j,"ID"]]["GO"].values
        new_rows = pandas.DataFrame({"GO":current_gos, "score": dist_df.loc[j,"dist"]*len(current_gos)})
        gos = gos.append(new_rows)
    gos_count = gos.groupby("GO").count().sort_values(by=["score"], ascending=False)
    pred_class_len = train_label_count.loc[dist_df.iloc[0,0]]
    ID = test_vec[0]
    pred_ID = "Mix"
    org_class = ",".join(test_label_df[test_label_df["ID"] == ID]["GO"].values)
    pred_class = ",".join(gos_count.index.values[0:pred_class_len])

    return [ID, pred_ID, org_class, pred_class]

def knn_vote_helper(args):
    return knn_vote(*args)

def main():

    global train_label_df
    global test_label_df
    global train_label_count

    process_options()

    k = 3

    train_vec_df = pandas.read_csv(train_vec_file, sep='\t' ,header=None)
    test_vec_df = pandas.read_csv(test_vec_file, sep='\t' ,header=None)
    train_label_df = pandas.read_csv(train_label_file, sep='\t' ,names=["ID","GO"])
    test_label_df = pandas.read_csv(test_label_file, sep='\t' ,names=["ID","GO"])

    train_label_count = train_label_df.groupby("ID").count()

    pred_res = pandas.DataFrame(columns=["ID","pred_ID","org_class","pred_class"])

    pool = multiprocessing.Pool()
    knn_args = []

    for i in range(0,len(test_vec_df.index)):
        knn_args.append([test_vec_df.loc[i], train_vec_df, k])

    p = multiprocessing.Pool()
    rs = p.map_async(knn_vote_helper, knn_args)
    p.close() # No more work
    while (True):
      if (rs.ready()): break
      remaining = rs._number_left
      print "Waiting for", remaining, "tasks to complete..."
      time.sleep(2)

    results = rs.get()
    for i in range(0,len(results)):
        pred_res.loc[i] = results[i]

    pred_res.to_csv(output_file, sep="\t", index=False)

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
