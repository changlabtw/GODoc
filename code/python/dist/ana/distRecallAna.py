import os
import sys
import pandas
import time
import multiprocessing
import numpy

global pred_res_file
global dist_df

def process_options(argv = sys.argv):
    global pred_res_file
    global output_path

    if len(argv) < 2:
		print "Usage: %s pred_res_file (output_path)" % argv[0]
		sys.exit(1)
    elif len(argv) == 2:
        pred_res_file = argv[1]
        output_path = ""
    elif len(argv) == 3:
        pred_res_file = argv[1]
        output_path = argv[2]

    if not os.path.exists(pred_res_file):
        print "pred_res_file not found."
        sys.exit(1)

def intersection(x,y):
    return (set(x) & set(y))

def fmeasure(r,p):
    if r+p == 0:
        return 0
    else:
        return (2*r*p)/(r+p)

def measure(ind):

    res_df = pandas.DataFrame(columns=["bucket","recall"])
    ID = dist_df.loc[ind,0].split(',')[0]
    org_class = dist_df.loc[ind,0].split(',')[1:]

    pred_class = []

    knn_df = pandas.DataFrame(columns=['ID','dist','gos'])
    for i in range(1,len(dist_df.loc[ind])):
        cur_ID = dist_df.loc[ind,i].split(',')[0]
        cur_dist = float(dist_df.loc[ind,i].split(',')[1])
        cur_gos = dist_df.loc[ind,i].split(',')[2:]
        knn_df.loc[i] = [cur_ID,cur_dist,cur_gos]

    knn_df['bucket'] = pandas.cut(knn_df["dist"], numpy.arange(0, 0.5, 0.02))

    for ind, bucket_range in enumerate(knn_df['bucket'].cat.categories.values):
        gos_list = knn_df[knn_df['bucket'] == bucket_range]['gos'].values
        for gos in gos_list:
            pred_class = numpy.union1d(gos,pred_class)
        recall = float(len(numpy.intersect1d(org_class,pred_class)))/float(len(org_class))
        res_df.loc[ind] = [bucket_range,recall]
        pred_class = numpy.intersect1d(org_class,pred_class)

    return res_df

def measure_helper(args):
    return measure(*args)

def main():

    global dist_df

    process_options()

    dist_df = pandas.read_csv(pred_res_file, sep="\t", header=None)

    measure_args = []
    for ind in range(0,len(dist_df.index)):
        measure_args.append([ind])

    pool = multiprocessing.Pool()
    p = multiprocessing.Pool()
    rs = p.map_async(measure_helper, measure_args)
    p.close() # No more work
    while (True):
      if (rs.ready()): break
      remaining = rs._number_left
      print "Waiting for", remaining, "tasks to complete..."
      time.sleep(2)

    res_df = pandas.DataFrame(columns=["bucket","recall"])
    results = rs.get()
    for i in range(0,len(results)):
        res_df = res_df.append(results[i])

    recall_mean = res_df.groupby('bucket').mean()
    fig = recall_mean.plot(kind='bar').get_figure()
    fig.savefig(os.path.basename(pred_res_file)+'_recall_mean.png')
    recall_std = res_df.groupby('bucket').std()
    fig = recall_std.plot(kind='bar').get_figure()
    fig.savefig(os.path.basename(pred_res_file)+'_recall_std.png')
    if output_path == "":
        output_file = os.path.basename(pred_res_file)+"_recall.tsv"
    else:
        output_file = output_path+'/'+os.path.basename(pred_res_file)+"_recall.tsv"
    recall_mean.to_csv(output_file,sep="\t")


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
