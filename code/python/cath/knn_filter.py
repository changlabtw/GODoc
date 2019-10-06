import os
import sys
import pandas
import time
import argparse
import multiprocessing
from collections import Counter

global args
global knn_df
global train_map_df
global target_map_df
global target_map_list

def process_options():
    global args

    parser = argparse.ArgumentParser(description='Get best result from hmmscan result.')
    parser.add_argument('-i', '--input', help='knn result')
    parser.add_argument('-train', '--train_map', help='train cath map tsv file')
    parser.add_argument('-target', '--target_map', help='target cath map tsv file')
    parser.add_argument('-sel', '--select', help='target cath map tsv file', choices=['sf','model','funfam'])
    parser.add_argument('-m', '--method', help='0:filt by target cath, 1:filt by 1NN cath, 2:filt by most commen cath', type=int)
    parser.add_argument('-o','--output',help='Output file name', default='filtered_knn.tsv')

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print "knn result hmmscan result not found."
        sys.exit(1)

    if not os.path.exists(args.train_map):
        print "train cath map tsv file not found."
        sys.exit(1)

    if not os.path.exists(args.target_map):
        print "target cath map tsv file not found."
        sys.exit(1)

    if os.path.exists(args.output):
        print "output allready exists."
        sys.exit(1)

def filter(target, select):
    global knn_df
    global train_map_df
    global target_map_df
    global target_map_list

    cur_pred_ID = [ x.split(',')[0] for x in knn_df[knn_df['ID'] == target]['pred_ID'].values[0].split(';') ]
    cur_pred_dist = [ x.split(',')[1] for x in knn_df[knn_df['ID'] == target]['pred_ID'].values[0].split(';') ]
    pred_cath = []
    for pred_ID in cur_pred_ID:
        col_index = train_map_df['query'] == pred_ID
        cur_pred_cath = train_map_df.loc[col_index,select].values
        if len(cur_pred_cath) == 0:
            pred_cath.append(None)
        elif len(cur_pred_cath) == 1:
            pred_cath.append(cur_pred_cath[0])
    target_cath = target_map_df[target_map_df['query']==target][select].values

    if (args.method == 0):
        # NN cath == target cath
        filtered_index = [ ind for ind,x in enumerate(pred_cath) if x in target_cath ]
        filtered_knn = zip([cur_pred_ID[ind] for ind in filtered_index],[cur_pred_dist[ind] for ind in filtered_index])
        filtered_knn = [','.join(x) for x in filtered_knn]
        filtered_knn = ';'.join(filtered_knn)
    elif (args.method == 1):
        # NN cath == 1NN cath
        pred_df = pandas.DataFrame({'ID':cur_pred_ID,'dist':cur_pred_dist})
        pred_df = pred_df.sort(['dist'],ascending=False).reset_index(drop=True)
        col_index = train_map_df['query'] == pred_df.loc[0,['ID']].values[0]
        target_cath = train_map_df.loc[col_index,select].values
        filtered_index = [ ind for ind,x in enumerate(pred_cath) if x in target_cath ]
        filtered_knn = zip([cur_pred_ID[ind] for ind in filtered_index],[cur_pred_dist[ind] for ind in filtered_index])
        filtered_knn = [','.join(x) for x in filtered_knn]
        filtered_knn = ';'.join(filtered_knn)
    elif (args.method == 2):
        # NN cath == most_common(NN) cath
        count = Counter(pred_cath)
        if count.most_common()[0][1] == 1:
            pred_df = pandas.DataFrame({'ID':cur_pred_ID,'dist':cur_pred_dist})
            pred_df = pred_df.sort(['dist'],ascending=False).reset_index(drop=True)
            col_index = train_map_df['query'] == pred_df.loc[0,['ID']].values[0]
            target_cath = train_map_df.loc[col_index,select].values
        else:
            target_cath = [count.most_common()[0][0]]
        filtered_index = [ ind for ind,x in enumerate(pred_cath) if x in target_cath ]
        filtered_knn = zip([cur_pred_ID[ind] for ind in filtered_index],[cur_pred_dist[ind] for ind in filtered_index])
        filtered_knn = [','.join(x) for x in filtered_knn]
        filtered_knn = ';'.join(filtered_knn)

    if (filtered_knn == ""):
        filtered_knn = knn_df[knn_df['ID'] == target]['pred_ID'].values[0]

    return [target, filtered_knn]

def filter_helper(args):
    return filter(*args)

def main():

    global knn_df
    global train_map_df
    global target_map_df
    global target_map_list

    process_options()

    knn_df = pandas.read_csv(args.input, sep='\t')
    train_map_df = pandas.read_csv(args.train_map, sep='\t', dtype={'query':str,'sf':str,'funfam':str,'model':str})
    target_map_df = pandas.read_csv(args.target_map, sep='\t', dtype={'query':str,'sf':str,'funfam':str,'model':str})
    target_map_list = target_map_df['query'].values

    filter_args = []

    for target in target_map_list:
        filter_args.append([target, args.select])

    pool = multiprocessing.Pool()
    p = multiprocessing.Pool()
    rs = p.map_async(filter_helper, filter_args)
    p.close() # No more work
    while (True):
      if (rs.ready()): break
      remaining = rs._number_left
      print "Waiting for", remaining, "tasks to complete..."
      time.sleep(2)

    results = rs.get()
    for row in results:
        row_index = knn_df.ID == row[0]
        knn_df.loc[row_index,'pred_ID'] = row[1]

    knn_df.to_csv(args.output, sep='\t', index=False)

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
