import os
import sys
import pandas
import time
import argparse

global args

def process_options():
    global args

    parser = argparse.ArgumentParser(description='PCA with nfold')
    parser.add_argument('-i','--vector_file', help='Training vector folder')
    parser.add_argument('-l','--list_file', help='ID list file')
    parser.add_argument('-o','--output',help='Output file name', default='filter_result.csv')

    args = parser.parse_args()

    if not os.path.exists(args.vector_file):
        print "vector_file not found."
        sys.exit(1)

    if not os.path.exists(args.list_file):
        print "list_file not found."
        sys.exit(1)

    if os.path.exists(args.output):
        print "output allready exists."
        sys.exit(1)

def main():

    process_options()

    vector_df = pandas.read_csv(args.vector_file, header=None)

    with open(args.list_file, 'r') as f:
        ID_list = f.read().splitlines()

    vector_df[vector_df[0].isin(ID_list)].to_csv(args.output, index=False, header=False)

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
