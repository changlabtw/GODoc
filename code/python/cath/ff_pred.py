import os
import sys
import pandas
import time
import multiprocessing
import argparse
import numpy as np

global args
global knn_df
global label_df
global train_hmm_df
global test_hmm_df
global target_list

def process_options():
    global args

    parser = argparse.ArgumentParser(description='Predict GO with CATH')
    parser.add_argument('-i', '--input', help='knn file')
    parser.add_argument('-l', '--label_file', help='Training label file')
    parser.add_argument('-test_m', '--test_map', help='hmmscan result dataframe pkl')
    parser.add_argument('-train_m', '--train_map', help='hmmscan result dataframe pkl')
    parser.add_argument('-t','--threshold',help='e-value threshold', type=float, default=1.0e-5)
    parser.add_argument('-o','--output',help='Output file name', default='ID_cath_map.tsv')

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print "knn result file not found."
        sys.exit(1)

    if not os.path.exists(args.label_file):
        print "label_file not found."
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

def ff_pred(ind, threshold):

    cur_ID = knn_df.loc[ind, 'ID']
    cur_pred_pairs = [ x.split(',') for x in knn_df.loc[ind, 'pred_ID'].split(';')]
    cur_pred_IDs = [ pair[0] for pair in cur_pred_pairs]
    if any([ p_id in train_list for p_id in cur_pred_IDs ]):
        target_df = train_hmm_df.loc[cur_pred_IDs]
        target_df = target_df[target_df['b_E-value']<threshold]
    else:
        print "No train ff " + cur_ID
        return None
    if cur_ID in target_list:
        try:
            cur_ID_ffs = test_hmm_df.loc[cur_ID]
            if type(cur_ID_ffs) == pandas.core.series.Series:
                if cur_ID_ffs['b_E-value'] < threshold:
                    cur_ID_ffs = []
                else:
                    cur_ID_ffs = cur_ID_ffs['target']
            else:
                cur_ID_ffs = cur_ID_ffs[cur_ID_ffs['b_E-value']<threshold]['target'].values
            dfs = []
            for ff in cur_ID_ffs:
                ff_protein = target_df[target_df['target'] == ff].index.unique()
                if len(ff_protein) != 0:
                    GO_sta = label_df[label_df['ID'].isin(ff_protein)].groupby("GO").count().apply(lambda x: x/x.count())
                    dfs.append(GO_sta)
            sta_df = None
            for ind, cur_df in enumerate(dfs):
                if ind == 0:
                    sta_df = cur_df
                else:
                    sta_df = pandas.merge(sta_df, cur_df, how='outer', left_index=True, right_index=True)
            sta_df['max'] = sta_df.apply(lambda x: x.max(), axis=1)
            sta_df['map_score'] = sta_df['max'].apply(lambda x: x/sta_df['max'].max())
            return [cur_ID, sta_df['map_score']]
        except AttributeError:
            print "AttributeError on " + cur_ID
            return None
        except KeyError:
            print "KeyError on " + cur_ID
            return None
    else:
        return None

def ff_pred_helper(args):
    return ff_pred(*args)

def main():

    global knn_df
    global label_df
    global train_hmm_df
    global test_hmm_df
    global target_list
    global train_list

    process_options()

    knn_df = pandas.read_csv(args.input, sep='\t')
    label_df = pandas.read_csv(args.label_file, sep='\t' ,names=["ID","GO"])
    test_hmm_df = pandas.read_pickle(args.test_map)
    train_hmm_df = pandas.read_pickle(args.train_map)

    target_list = test_hmm_df.index.unique()
    train_list = train_hmm_df.index.unique()

    ff_pred_args = []
    for ind in range(0,len(knn_df)):
        ff_pred_args.append([ind, args.threshold])

    pool = multiprocessing.Pool()
    p = multiprocessing.Pool()
    rs = p.map_async(ff_pred_helper, ff_pred_args)
    p.close() # No more work
    while (True):
      if (rs.ready()): break
      remaining = rs._number_left
      print "Waiting for", remaining, "tasks to complete..."
      time.sleep(2)

    results = rs.get()
    with open(args.output, 'w') as f:
        f.write("AUTHOR TEAM_NAME\n")
        f.write("MODEL 1\n")
        f.write("KEYWORDS\tFunFam predict\n")
        for res in results:
            if res != None:
                for ind in range(0,len(res[1])):
                    f.write(res[0])
                    f.write('\t')
                    f.write(res[1].index[ind])
                    f.write('\t')
                    f.write(str(res[1].iloc[ind]))
                    f.write('\n')

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
