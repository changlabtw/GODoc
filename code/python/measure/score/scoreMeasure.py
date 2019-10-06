import os
import sys
import pandas
import time
import multiprocessing


global res_file
global output_file
global step_size
global label_file
global res_df
global label_df

def process_options(argv = sys.argv):
    global res_file
    global output_file
    global step_size
    global label_file

    if len(argv) < 4:
		print "Usage: %s res_file label_file output_file (step_size)" % argv[0]
		sys.exit(1)
    elif len(argv) == 4:
        res_file = argv[1]
        label_file = argv[2]
        output_file = argv[3]
        step_size = 0.05
    elif len(argv) == 5:
        res_file = argv[1]
        label_file = argv[2]
        output_file = argv[3]
        step_size = float(argv[4])

    if not os.path.exists(res_file):
        print "res_file not found."
        sys.exit(1)

    if not os.path.exists(label_file):
        print "label_file not found."
        sys.exit(1)

def intersection(x,y):
    return (set(x) & set(y))

def fmeasure(x):
    if x['reacll']+x['precision'] == 0:
        return 0
    else:
        return (2*x['reacll']*x['precision'])/(x['reacll']+x['precision'])

def measure(threshold, amount):

    df = pandas.DataFrame(columns=['ID','org_class','pred_class'])
    current_df = res_df[ res_df['score']>=threshold ]
    IDs = current_df['ID'].unique()
    unpred = amount - len(IDs)
    for ID in IDs:
        org_class = label_df[ label_df['ID'] == ID ]['GO'].values
        pred_class = current_df[ current_df['ID'] == ID ]['GO'].values
        df.loc[len(df.index)] = [ID, org_class, pred_class]

    df['reacll'] = df.apply(lambda x: float(len(intersection(x['org_class'],x['pred_class'])))/float(len(x['org_class'])), axis=1)
    df['precision'] = df.apply(lambda x: float(len(intersection(x['org_class'],x['pred_class'])))/float(len(x['pred_class'])), axis=1)
    df['f-measure'] = df.apply(fmeasure , axis=1)

    # print "current threshold %s:" % threshold
    # print "overall"
    r = df['reacll'].sum()/len(df.index)
    p = df['precision'].sum()/len(df.index)
    # print "recall:\t" + str(r)
    # print "precision:\t" + str(p)
    # print "f-measure:\t" + str((2*r*p)/(r+p))
    # print "coverage:\t" + str(round(float(1) - float(unpred)/float(amount), 3))

    return [threshold,r,p,(2*r*p)/(r+p),round(float(1) - float(unpred)/float(amount), 3)]

def measure_vote_helper(args):
    return measure(*args)

def main():

    global res_df
    global label_df

    process_options()

    res_df = pandas.read_csv(res_file, sep='\t' ,names=['ID','GO','score'] ,skiprows=3 ,skipfooter=1, engine='python')
    label_df = pandas.read_csv(label_file, sep='\t' ,names=['ID','GO'] )
    res_df = res_df[res_df['ID'].isin(label_df['ID'].unique())]

    amount = len(label_df['ID'].unique())

    pool = multiprocessing.Pool()
    measure_args = []

    for i in range(0,int(1/step_size)+1):
        measure_args.append([i*step_size, amount])

    p = multiprocessing.Pool()
    rs = p.map_async(measure_vote_helper, measure_args)
    p.close() # No more work
    while (True):
      if (rs.ready()): break
      remaining = rs._number_left
      print "Waiting for", remaining, "tasks to complete..."
      time.sleep(2)

    results = rs.get()
    measure_df = pandas.DataFrame(columns=["threshold","recall","precision","f-measure","coverage"])
    for i in range(0,len(results)):
        measure_df.loc[i] = results[i]

    print measure_df.sort_values('threshold')
    print "Max f-measure: %s" % measure_df['f-measure'].max()

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
