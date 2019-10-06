import os
import sys
import pandas
import time
import multiprocessing
import argparse

global args
global hmm_df

def process_options():
    global args

    parser = argparse.ArgumentParser(description='Convert hmm scan result to pandas dataframe pickle file.')
    parser.add_argument('-i', '--input', help='hmmscan result')
    parser.add_argument('-o','--output',help='Output file name', default='hmm.pkl')

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print "input hmmscan result not found."
        sys.exit(1)

    if os.path.exists(args.output):
        print "output allready exists."
        sys.exit(1)

def main():

    global hmm_df

    process_options()

    col = ['target', 'target_accession', 'query', 'query_accession', 'f_E-value', 'f_score', 'f_bias',
           'b_E-value', 'b_score', 'b_bias', 'exp', 'reg', 'clu', 'ov', 'env', 'dom', 'rep', 'inc',
           ' description']

    hmm_df = pandas.read_csv(args.input, delim_whitespace=True, comment='#', names=col, engine='python')

    hmm_df = hmm_df.loc[:,['target','query','f_E-value','b_E-value']]
    hmm_df['target'] = hmm_df['target'].apply(lambda x: x.split('/')[2])
    hmm_df = hmm_df.set_index(['query'])
    hmm_df = hmm_df.sort_index()

    hmm_df.to_pickle(args.output)

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
