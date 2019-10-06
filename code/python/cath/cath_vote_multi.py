import os
import sys
import pandas
import numpy
import time
import multiprocessing
import argparse

global args
global knn_df
global label_df

def process_options(argv = sys.argv):
    global args

    parser = argparse.ArgumentParser(description='Vote by knn file with cath filter.')
    parser.add_argument('-i', '--knn_file', help='KNN file')
    parser.add_argument('-l', '--label_file', help='Training label file')
    parser.add_argument('-m', '--method', help='Score method, 0:score=count/max(count), 1:score=1.00', type=int, choices=[0,1,2], default=1)
    parser.add_argument('-t', '--threshold', help='threshold for method 0, frequence >= threshold', type=float, default=0.5)
    parser.add_argument('-o','--output_file',help='Output file name', default='vote_score.txt')

    args = parser.parse_args()

    if not os.path.exists(args.knn_file):
        print "knn_file not found."
        sys.exit(1)

    if not os.path.exists(args.label_file):
        print "label_file not found."
        sys.exit(1)

    if os.path.exists(args.output_file):
        print "output_file already exits."
        sys.exit(1)

def series_sum(series_list):
    res = pandas.Series([])
    for l in series_list:
        res = res.add(l,fill_value=0)
    return res

def fun_search(ID):
    global label_df
    return pandas.Series(label_df[label_df['ID'].searchsorted(ID, 'left')[0]:label_df['ID'].searchsorted(ID, 'right')[0]]['GO']).values

def vote(i):

    global knn_df
    global label_df

    threshold = args.threshold

    if args.method == 2:
        # if knn_df.loc[i,'count_max'] >= 1:
        #     pred_GO_list = [ label_df[label_df['ID']==ID]['GO'].values for ID in [ pair.split(',')[0] for pair in knn_df.loc[i,'pred_ID'].split(';') ]]
        #     cur_sta = series_sum([pandas.Series(l).value_counts()*knn_df.loc[i,'count_list'][ind] for ind,l in enumerate(pred_GO_list)])
        #     pred_pairs = zip(cur_sta.index, cur_sta/cur_sta.max())
        if knn_df.values[i,4] >= 1:
            pred_GO_list = [ fun_search(ID) for ID in [ pair.split(',')[0] for pair in knn_df.values[i,1].split(';') ]]
            cur_sta = series_sum([pandas.Series(l).value_counts()*knn_df.values[i,2][ind] for ind,l in enumerate(pred_GO_list)])
            pred_pairs = zip(cur_sta.index, cur_sta/cur_sta.max())
        else:
            # skip pred if intersection amout = 0
            return []
            # cur_pred_IDs = [(knn_df.loc[i,'pred_ID'].split(';')[knn_df.loc[i,'dist_list'].index(knn_df.loc[i,'dist_min'])]).split(',')[0]]
            # pred_GOs = label_df[label_df['ID'].isin(cur_pred_IDs)]['GO'].values
            # pred_pairs = [ [GO,'1.00'] for GO in pred_GOs ]
    else:
        if knn_df.loc[i,'count_max'] >= 1:
            cur_pred_IDs = [ pair.split(',')[0] for pair in knn_df.loc[i,'pred_ID'].split(';') ]
        else:
            cur_pred_IDs = [(knn_df.loc[i,'pred_ID'].split(';')[knn_df.loc[i,'dist_list'].index(knn_df.loc[i,'dist_min'])]).split(',')[0]]
        pred_GOs = label_df[label_df['ID'].isin(cur_pred_IDs)]['GO'].values
        cur_sta = pandas.Series(pred_GOs).value_counts()
        if args.method == 0:
            pred_pairs = zip(cur_sta.index, cur_sta/cur_sta.max())
        elif args.method ==1:
            pred_GOs = list(cur_sta[cur_sta/(cur_sta.max())>=threshold].index)
            pred_pairs = [ [GO,'1.00'] for GO in pred_GOs ]

    return [knn_df.values[i,0], pred_pairs]

def vote_helper(args):
    return vote(*args)

def main():

    global knn_df
    global label_df

    process_options()

    threshold = 0.5
    knn_df = pandas.read_csv(args.knn_file, sep='\t' ,header=0)
    label_df = pandas.read_csv(args.label_file, sep='\t' ,names=["ID","GO"])
    label_df = label_df.sort_values("ID")

    print "Unpred protein amount: %i" % len(knn_df[knn_df['pred_ID'].isnull()].index)
    knn_df = knn_df[-knn_df['pred_ID'].isnull()].reset_index(drop=True) #drop unpred protein

    knn_df['count_list'] = knn_df['pred_ID'].apply(lambda x: [int(pair.split(',')[2]) for pair in x.split(';')] )
    knn_df['dist_list'] = knn_df['pred_ID'].apply(lambda x: [float(pair.split(',')[1]) for pair in x.split(';')] )
    knn_df['count_max'] = knn_df['count_list'].apply(lambda x: max(x) )
    knn_df['dist_min'] = knn_df['dist_list'].apply(lambda x: min(x) )

    pool = multiprocessing.Pool()
    vote_args = []

    for i in range(0,len(knn_df)):
        vote_args.append([i])

    p = multiprocessing.Pool()
    rs = p.map_async(vote_helper, vote_args)
    p.close() # No more work
    while (True):
      if (rs.ready()): break
      remaining = rs._number_left
      print "Waiting for", remaining, "tasks to complete..."
      time.sleep(2)

    with open(args.output_file, 'w') as f:
        f.write("AUTHOR TEAM_NAME\n")
        f.write("MODEL 1\n")
        f.write("KEYWORDS\tCATH Vote\n")
        results = rs.get()
        for rows in results:
            if len(rows) != 0:
                for row in rows[1]:
                    f.write(rows[0])
                    f.write('\t')
                    f.write(row[0])
                    f.write('\t')
                    f.write(str(row[1]))
                    f.write('\n')
        f.write("END\n")

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
