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

def measure(ind,threshold,pred_len):

    res = []
    ID = dist_df.loc[ind,0].split(',')[0]
    org_class = dist_df.loc[ind,0].split(',')[1:]
    gos = pandas.DataFrame(columns=["GO","score"])
    for i in range(1,len(dist_df.loc[ind])):
        if float(dist_df.loc[ind,i].split(',')[1]) <= threshold or i ==1:
            cur_ID = dist_df.loc[ind,i].split(',')[0]
            cur_dist = float(dist_df.loc[ind,i].split(',')[1])
            cur_gos = dist_df.loc[ind,i].split(',')[2:]
            score = numpy.sqrt(1/cur_dist) # sqrt version score
            # score = numpy.log(1/cur_dist) # log version score
            new_rows = pandas.DataFrame({"GO":cur_gos, "score": [score]*len(cur_gos) })
            gos = gos.append(new_rows)
        else:
            break;
    gos = gos.groupby(['GO']).sum().sort_values(by=["score"], ascending=False)
    pred_class = gos.index.values[0:pred_len]
    recall = float(len(numpy.intersect1d(org_class,pred_class)))/float(len(org_class))
    precision = float(len(numpy.intersect1d(org_class,pred_class)))/float(len(pred_class))
    return [ID,threshold,pred_len,recall,precision]

def measure_helper(args):
    return measure(*args)

def main():

    global train_label_df
    global test_label_df
    global dist_df

    min_threshold = 0.05
    max_threshold = 0.151
    threshold_step_size = 0.01
    min_pred_len = 2
    max_pred_len = 6

    process_options()

    dist_df = pandas.read_csv(pred_res_file, sep="\t", header=None)

    measure_args = []
    for ind in range(0,len(dist_df.index)):
        for threshold in numpy.arange(min_threshold,max_threshold,threshold_step_size):
            for pred_len in range(min_pred_len,max_pred_len+1):
                measure_args.append([ind, threshold, pred_len])

    pool = multiprocessing.Pool()
    p = multiprocessing.Pool()
    rs = p.map_async(measure_helper, measure_args)
    p.close() # No more work
    while (True):
      if (rs.ready()): break
      remaining = rs._number_left
      print "Waiting for", remaining, "tasks to complete..."
      time.sleep(2)

    res_df = pandas.DataFrame(columns=["ID","threshold","pred_len","recall","precision"])
    results = rs.get()
    for i in range(0,len(results)):
        res_df.loc[i] = results[i]

    report_df = pandas.DataFrame(columns=["threshold","pred_len","recall","precision","fmeasure"])
    for threshold in numpy.arange(min_threshold,max_threshold,threshold_step_size):
        cur_threshold = res_df[ res_df["threshold"] == threshold ]
        for pred_len in range(min_pred_len,max_pred_len+1):
            cur_df = cur_threshold[ cur_threshold["pred_len"] == pred_len ]
            recall = (cur_df['recall'].sum()/len(cur_df.index))
            precision = (cur_df['precision'].sum()/len(cur_df.index))
            fm = fmeasure(recall,precision)
            report_df.loc[len(report_df.index)] = [threshold,pred_len,recall,precision,fm]
    report_df = report_df.sort_values(by=["fmeasure"], ascending=False)
    print report_df
    if output_path == "":
        output_file = os.path.basename(pred_res_file)+"_res.tsv"
    else:
        output_file = output_path+'/'+os.path.basename(pred_res_file)+"_res.tsv"
    report_df.to_csv(output_file,sep="\t")


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
