import os
import sys
import pandas
import time
import argparse

global args

def process_options():

    global args

    parser = argparse.ArgumentParser(description='Get average pr-curve')
    parser.add_argument('-v','--pr_files', help='pr-curve files', nargs='+')
    parser.add_argument('-o','--output_file',help='Output file name', default='prcurve.csv')

    args = parser.parse_args()

    for f in args.pr_files:
        if not os.path.exists(f):
            print f + " not found."
            sys.exit(1)

    if os.path.exists(args.output_file):
        print "output_file already exists."
        sys.exit(1)

def main():

    process_options()

    prcurve_dfs = []
    for f in args.pr_files:
        prcurve_dfs.append(pandas.read_csv(f))

    res_df = pandas.DataFrame(columns=['precision','recall'])
    for i in range(0,len(prcurve_dfs[0])):
        cur_pr = 0
        cur_rc = 0
        for cur_df in prcurve_dfs:
            cur_pr = cur_pr + cur_df.loc[i,'precision']
            cur_rc = cur_rc + cur_df.loc[i,'recall']
        cur_pr = cur_pr/len(prcurve_dfs)
        cur_rc = cur_rc/len(prcurve_dfs)
        res_df.loc[i] = [cur_pr,cur_rc]

    res_df.to_csv(args.output_file, index=False)

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
