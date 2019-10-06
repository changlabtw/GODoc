import os
import sys
import pandas
import time
import multiprocessing
import numpy as np
import argparse

global fixed_score_df
global fixed_knn_res
global dynamic_score_df
global dynamic_knn_res
global args

def process_options():
    global args

    parser = argparse.ArgumentParser(description='Merge fixed-knn and dynamic-knn.')
    parser.add_argument('-fs', '--fixed_score', help='Fixed KNN vote score')
    parser.add_argument('-fk', '--fixed_knn', help='Fixed 10 NN result')
    parser.add_argument('-ds', '--dynamic_score', help='Dynamic KNN vote score')
    parser.add_argument('-dk', '--dynamic_knn', help='Dynamic KNN result')
    parser.add_argument('-k','--k',help='KNN number', type=int, default=1)
    parser.add_argument('-m','--method',help='Merge method, based on fixed or dynamic', type=str, choices=['fixed','dynamic'], required=True)
    parser.add_argument('-o','--output',help='Output file name', default='hybrid_KNN_vote_score.tsv')

    args = parser.parse_args()

    if not os.path.exists(args.fixed_score):
        print "fixed_score not found."
        sys.exit(1)

    if not os.path.exists(args.fixed_knn):
        print "fixed_knn not found."
        sys.exit(1)

    if not os.path.exists(args.dynamic_score):
        print "dynamic_score not found."
        sys.exit(1)

    if not os.path.exists(args.dynamic_knn):
        print "dynamic_score not found."
        sys.exit(1)

    if os.path.exists(args.output):
        print "output allready exists."
        sys.exit(1)

def score_search(score_df, ID):
    return score_df[score_df['ID'].searchsorted(ID, 'left')[0]:score_df['ID'].searchsorted(ID, 'right')[0]].values

def knn_merge(ID, k):

    global fixed_score_df
    global fixed_knn_res
    global dynamic_score_df
    global dynamic_knn_res

    for row in dynamic_knn_res:
        if row[0] == ID:
            nn_amount = row[1].count(';') + 1
            if nn_amount > k:
                return score_search(dynamic_score_df, ID)
            elif nn_amount == k:
                if args.method == 'fixed':
                    return score_search(fixed_score_df, ID)
                elif args.method == 'dynamic':
                    return score_search(dynamic_score_df, ID)
            else:
                return score_search(fixed_score_df, ID)
    for row in fixed_knn_res:
        if row[0] == ID:
            return score_search(fixed_score_df, ID)

def knn_merge_helper(args):
    return knn_merge(*args)

def main():

    global fixed_score_df
    global fixed_knn_res
    global dynamic_score_df
    global dynamic_knn_res

    process_options()

    fixed_score_df = pandas.read_csv(args.fixed_score, sep='\t', names=['ID','GO','score'], skiprows=3, skipfooter=1)
    fixed_score_df = fixed_score_df.sort_values("ID")
    dynamic_score_df = pandas.read_csv(args.dynamic_score, sep='\t', names=['ID','GO','score'], skiprows=3, skipfooter=1)
    dynamic_score_df = dynamic_score_df.sort_values("ID")
    fixed_knn_res = []
    with open(args.fixed_knn, 'r') as f:
        lines = f.read().splitlines()
        for line in lines[1:]:
            cur_row = line.split('\t')
            if len(cur_row) == 2:
                fixed_knn_res.append([cur_row[0],cur_row[1]])
    dynamic_knn_res = []
    with open(args.dynamic_knn, 'r') as f:
        lines = f.read().splitlines()
        for line in lines[1:]:
            cur_row = line.split('\t')
            if len(cur_row) == 2:
                dynamic_knn_res.append([cur_row[0],cur_row[1]])

    ID_list = [ row[0] for row in fixed_knn_res]

    knn_merge_args = []
    for ID in ID_list:
        knn_merge_args.append([ID, args.k])

    pool = multiprocessing.Pool()
    p = multiprocessing.Pool()
    rs = p.map_async(knn_merge_helper, knn_merge_args)
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
        f.write("KEYWORDS\thybrid-KNN\n")
        for rows in results:
            for row in rows:
                f.write('\t'.join(map(str,row)))
                f.write('\n')
        f.write('END\n')


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
