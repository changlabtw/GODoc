import os
import sys
import pandas
import time
import multiprocessing
import numpy
import math
from goatools.obo_parser import GODag, GraphEngines
import argparse

global args
global pred_res_df
global go_rel_file

def process_options():
    global args

    parser = argparse.ArgumentParser(description='Get predict GO\'s parents of GO term.')
    parser.add_argument('-i', '--pred_res_file', help='CAFA2 format result')
    parser.add_argument('-r', '--go_rel_file', help='GO relation file')
    parser.add_argument('-o', '--output_file', help='Predict result with inrich', default='inrich_result.txt')

    args = parser.parse_args()

    if not os.path.exists(args.pred_res_file):
        print "pred_res_file not found."
        sys.exit(1)

    if not os.path.exists(args.go_rel_file):
        print "go_rel_file not found."
        sys.exit(1)

    if os.path.exists(args.output_file):
        print "output_file already exists."
        sys.exit(1)

def find(ID):

    current_df = pred_res_df[pred_res_df['ID']==ID].reset_index(drop=True)
    propagated_df = pandas.DataFrame(columns=['GO','score'])

    for i in range(0,len(current_df.index)):
        current_leaf = current_df.loc[i,'GO']
        current_score = current_df.loc[i,'score']
        current_inrich = go_rel_file[go_rel_file['GO'] == current_leaf]['rel'].values
        if len(current_inrich) != 0:
            current_inrich = [ l.split(',') for l in filter(None,current_inrich[0].split(';')) ]
            current_inrich_go = [l[0] for l in current_inrich]
            current_inrich_score = [float(l[1])*current_score for l in current_inrich]
            current_list = [current_leaf] + current_inrich_go
            current_list_score = [current_score] + current_inrich_score
            new_rows = pandas.DataFrame({'ID':[ID] * len(current_list), 'GO':current_list, 'score':current_list_score })
            propagated_df = propagated_df.append(new_rows)
        else:
            new_rows = pandas.DataFrame({'ID':[ID], 'GO':[current_leaf], 'score':[current_score] })
            propagated_df = propagated_df.append(new_rows)

    propagated_df = propagated_df.groupby("GO").max().reset_index()
    propagated_df = propagated_df[propagated_df['score']>=0.01].reset_index(drop=True)

    return [propagated_df['ID'].values, propagated_df['GO'].values, propagated_df['score'].values]

def find_helper(args):
    return find(*args)

def main():

    global pred_res_df
    global go_rel_file

    process_options()

    pred_res_df = pandas.read_csv(args.pred_res_file, sep="\t", names=['ID','GO','score'], engine='python', skiprows=3, skipfooter=1)
    go_rel_file = pandas.read_csv(args.go_rel_file, sep='\t')

    find_args = []
    for ID in pred_res_df['ID'].unique():
        find_args.append([ID])

    pool = multiprocessing.Pool()
    p = multiprocessing.Pool()
    rs = p.map_async(find_helper, find_args)
    p.close() # No more work
    while (True):
      if (rs.ready()): break
      remaining = rs._number_left
      print "Waiting for", remaining, "tasks to complete..."
      time.sleep(2)


    results = rs.get()
    with open(args.output_file, 'w') as f:
        f.write("AUTHOR TEAM_NAME\n")
        f.write("MODEL 1\n")
        f.write("KEYWORDS\tpropagate\n")
        for rows in results:
            for i in range(0,len(rows[0])):
                f.write(rows[0][i])
                f.write('\t')
                f.write(rows[1][i])
                f.write('\t')
                f.write(str(rows[2][i]))
                f.write('\n')
        f.write("END\n")

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
