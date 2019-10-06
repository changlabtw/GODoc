import os
import sys
import pandas
import time
import multiprocessing
import argparse
import numpy as np

global args
global knn_df
global train_hmm_df
global test_hmm_df
global target_list

def process_options():
    global args

    parser = argparse.ArgumentParser(description='Filt knn result by funfam hmmscan result.')
    parser.add_argument('-i', '--input', help='knn file')
    parser.add_argument('-test_m', '--test_map', help='hmmscan result dataframe pkl')
    parser.add_argument('-train_m', '--train_map', help='hmmscan result dataframe pkl')
    parser.add_argument('-t','--threshold',help='e-value threshold', type=float, default=1.0e-5)
    parser.add_argument('-o','--output',help='Output file name', default='ID_cath_map.tsv')

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print "knn result file not found."
        sys.exit(1)

    if not os.path.exists(args.test_map):
        print "hmmscan result dataframe pkl file not found."
        sys.exit(1)

    if not os.path.exists(args.train_map):
        print "hmmscan result dataframe pkl file not found."
        sys.exit(1)

    if os.path.exists(args.output):
        print "output allready exists."
        sys.exit(1)

def ff_search(ff_df, ID):
    return ff_df[ff_df.index.searchsorted(ID, 'left'):ff_df.index.searchsorted(ID, 'right')]

def ff_filter(ind, threshold):

    # cur_ID = knn_df.loc[ind, 'ID']
    cur_ID = knn_df.values[ind, 0]
    # cur_pred_pairs = [ x.split(',') for x in knn_df.loc[ind, 'pred_ID'].split(';')]
    cur_pred_pairs = [ x.split(',') for x in knn_df.values[ind, 1].split(';')]
    if cur_ID in target_list:
        try:
            new_pairs = []
            # cur_ID_ffs = test_hmm_df[ (test_hmm_df['query'] == cur_ID)]
            # cur_ID_ffs = cur_ID_ffs[cur_ID_ffs['b_E-value'] < threshold]['target'].values
            # cur_ID_ffs = [ff for ff in test_hmm_df.loc[cur_ID].apply(lambda x: x['target'] if x['b_E-value']<threshold else None , axis=1).values if ff is not None]
            cur_ID_ffs = ff_search(test_hmm_df, cur_ID)
            if type(cur_ID_ffs) == pandas.core.series.Series:
                if cur_ID_ffs['b_E-value'] < threshold:
                    cur_ID_ffs = []
                else:
                    cur_ID_ffs = cur_ID_ffs['target']
            else:
                cur_ID_ffs = cur_ID_ffs[cur_ID_ffs['b_E-value']<threshold]['target'].values
            for pair in cur_pred_pairs:
                cur_pred_ID = pair[0]
                if cur_pred_ID in train_list:
                    #cur_pred_ID_ffs = train_hmm_df[ (train_hmm_df['query'] == cur_pred_ID)]
                    #cur_pred_ID_ffs = cur_pred_ID_ffs[cur_pred_ID_ffs['b_E-value'] < threshold]['target'].values
                    # cur_pred_ID_ffs = [ff for ff in train_hmm_df.loc[cur_pred_ID].apply(lambda x: x['target'] if x['b_E-value']<threshold else None , axis=1).values if ff is not None]
                    cur_pred_ID_ffs = ff_search(train_hmm_df, cur_pred_ID)
                    if type(cur_pred_ID_ffs) == pandas.core.series.Series:
                        if cur_pred_ID_ffs['b_E-value'] < threshold:
                            cur_pred_ID_ffs = []
                        else:
                            cur_pred_ID_ffs = cur_pred_ID_ffs['target']
                    else:
                        cur_pred_ID_ffs = cur_pred_ID_ffs[cur_pred_ID_ffs['b_E-value']<threshold]['target'].values
                    ff_intersect = len(np.intersect1d(cur_ID_ffs,cur_pred_ID_ffs))
                else:
                    ff_intersect = 0
                new_pairs.append(','.join(pair+[str(ff_intersect)]))
        except TypeError:
            print cur_ID
            print cur_ID_ffs
            print cur_pred_ID
            print train_hmm_df.loc[cur_pred_ID]

        return [cur_ID, ';'.join(new_pairs)]
    else:
        return [cur_ID, ';'.join([ ','.join(x+['-1']) for x in cur_pred_pairs ]) ]

def ff_filter_helper(args):
    return ff_filter(*args)

def main():

    global knn_df
    global train_hmm_df
    global test_hmm_df
    global target_list
    global train_list

    process_options()

    knn_df = pandas.read_csv(args.input, sep='\t')
    test_hmm_df = pandas.read_pickle(args.test_map)
    test_hmm_df = test_hmm_df.sort_index()

    train_hmm_df = pandas.read_pickle(args.train_map)
    train_hmm_df = train_hmm_df.sort_index()

    target_list = test_hmm_df.index.unique()
    train_list = train_hmm_df.index.unique()

    ff_filter_args = []
    for ind in range(0,len(knn_df)):
        ff_filter_args.append([ind, args.threshold])

    pool = multiprocessing.Pool()
    p = multiprocessing.Pool()
    rs = p.map_async(ff_filter_helper, ff_filter_args)
    p.close() # No more work
    while (True):
      if (rs.ready()): break
      remaining = rs._number_left
      print "Waiting for", remaining, "tasks to complete..."
      time.sleep(2)

    results = rs.get()
    with open(args.output, 'w') as f:
        f.write('ID\tpred_ID\n')
        for row in results:
            f.write(row[0])
            f.write('\t')
            f.write(row[1])
            f.write('\n')

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
