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

    parser = argparse.ArgumentParser(description='Get best result from hmmscan result.')
    parser.add_argument('-i', '--input', help='hmmscan result')
    parser.add_argument('-n','--n',help='Top N number', type=int, default=1)
    parser.add_argument('-t','--threshold',help='e-value threshold', type=int, default=1)
    parser.add_argument('-o','--output',help='Output file name', default='ID_cath_map.tsv')

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print "input hmmscan result not found."
        sys.exit(1)

    if os.path.exists(args.output):
        print "output allready exists."
        sys.exit(1)

def hmm_filter(target_ID):

    ff = hmm_df[hmm_df['query'] == target_ID].sort_values('b_E-value').iloc[0,0].split('/')[2]

    return [target_ID,ff]

def hmm_filter_helper(args):
    return hmm_filter(*args)

def main():

    global hmm_df

    process_options()

    col = ['target', 'target_accession', 'query', 'query_accession', 'f_E-value', 'f_score', 'f_bias',
           'b_E-value', 'b_score', 'b_bias', 'exp', 'reg', 'clu', 'ov', 'env', 'dom', 'rep', 'inc',
           ' description']

    hmm_df =  pandas.read_csv(args.input, delim_whitespace=True, comment='#', names=col, engine='python')

    target_list = hmm_df['query'].unique()

    hmm_filter_args = []
    for target_ID in target_list:
        hmm_filter_args.append([target_ID])

    pool = multiprocessing.Pool()
    p = multiprocessing.Pool()
    rs = p.map_async(hmm_filter_helper, hmm_filter_args)
    p.close() # No more work
    while (True):
      if (rs.ready()): break
      remaining = rs._number_left
      print "Waiting for", remaining, "tasks to complete..."
      time.sleep(2)

    results = rs.get()
    with open(args.output, 'w') as f:
        f.write('ID\tff\n')
        for row in results:
            f.write(row[0])
            f.write('\t')
            f.write(row[1])
            f.write('\n')

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
