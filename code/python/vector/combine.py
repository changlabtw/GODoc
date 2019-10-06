import os
import sys
import pandas
import time
import argparse

global args

def process_options():

    global args

    parser = argparse.ArgumentParser(description='Combine vector')
    parser.add_argument('-v','--vector_files', help='Vector files', nargs='+')
    parser.add_argument('-o','--output_file',help='Output file name', default='combine_vec.csv')

    args = parser.parse_args()

    for f in args.vector_files:
        if not os.path.exists(f):
            print f + " not found."
            sys.exit(1)

    if os.path.exists(args.output_file):
        print "output_file already exists."
        sys.exit(1)

def main():

    process_options()

    vector_dfs = []
    for f in args.vector_files:
        vector_dfs.append(pandas.read_csv(f, header=None))

    res_df = None
    for vec_df in vector_dfs:
        if not isinstance(res_df, pandas.core.frame.DataFrame):
            res_df = vec_df
        else:
            res_df = pandas.merge(res_df, vec_df, how='inner', on=[0])

    res_df.to_csv(args.output_file, index=False, header=False)

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
