import os
import sys
import pandas
import time
import numpy as np
import argparse

global train_vec_df
global test_vec_df
global base_vec_df
global tree
global args

def process_options():
    global args

    parser = argparse.ArgumentParser(description='Split Dynamic KNN Q3 to Q2 or Q1')
    parser.add_argument('-b', '--base_knn_file', help='Training 1NN result')
    parser.add_argument('-i', '--input_knn_result', help='Q3 KNN result')
    parser.add_argument('-q', '--q', choices=[1,2], type=int, required=True, help='1:Q1, 2:Q2')
    parser.add_argument('-o','--output',help='Output file name', default='pred_res.tsv')

    args = parser.parse_args()

    if not os.path.exists(args.base_knn_file):
        print "base_knn_file not found."
        sys.exit(1)

    if not os.path.exists(args.input_knn_result):
        print "input_knn_result not found."
        sys.exit(1)

    if os.path.exists(args.output):
        print "output allready exists."
        sys.exit(1)

def main():

    process_options()

    #Find distance threshold
    base_knn_df = pandas.read_csv(args.base_knn_file, sep='\t' ,header=0)
    base_knn_df['dist'] = base_knn_df['pred_ID'].apply(lambda x: float(x.split(';')[0].split(',')[1]))

    q_list = ['25%','50%']

    threshold = base_knn_df['dist'].describe()[q_list[args.q-1]]

    with open(args.input_knn_result, 'r') as f:
        lines = f.read().splitlines()

    with open(args.output, 'w') as f:
        f.write('ID\tpred_ID\n')
        for i in range(1,len(lines)):
            ID = lines[i].split('\t')[0]
            pairs = lines[i].split('\t')[1]
            pairs = [ [ pair.split(',')[0], float(pair.split(',')[1]) ] for pair in pairs.split(';') ]
            pairs = [ pair for pair in pairs if pair[1]<threshold ]
            if len(pairs) != 0:
                f.write(ID)
                f.write('\t')
                f.write(';'.join([','.join([pair[0],str(pair[1])]) for pair in pairs]))
                f.write('\n')

    # knn_df = pandas.read_csv(args.input_knn_result, sep='\t', header=0)
    # knn_df['pred_pair'] = knn_df['pred_ID'].apply(lambda x: [ [ pair.split(',')[0], float(pair.split(',')[1]) ] for pair in x.split(';') ])
    # knn_df['new_pred'] = knn_df['pred_pair'].apply(lambda x: [ pair for pair in x if pair[1]<threshold ])
    #
    # with open(args.output, 'w') as f:
    #     f.write('ID\tpred_ID\n')
    #     for i in range(0,len(knn_df)):
    #         if len(knn_df.loc[i,'new_pred']) != 0:
    #             f.write(knn_df.loc[i,'ID'])
    #             f.write('\t')
    #             f.write(';'.join([','.join([pair[0],str(pair[1])]) for pair in knn_df.loc[i,'new_pred']]))
    #             f.write('\n')

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
