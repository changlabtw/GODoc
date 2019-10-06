import os
import sys
import time
import pandas
import argparse
import numpy as np

global args

def process_options():
    global args

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i','--input', help='superfamily to go map file')

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print "superfamily to go map file not found."
        sys.exit(1)

def main():

    process_options()

    input_df = pandas.read_csv(args.input, sep='\t', names=['sf','GO','type','value'])
    bpo_df = input_df[input_df['type'] == 'P']
    cco_df = input_df[input_df['type'] == 'C']
    mfo_df = input_df[input_df['type'] == 'F']

    bpo_df.to_csv('bpo_superfamily_go.tsv', sep='\t', index=False, header=False)
    cco_df.to_csv('cco_superfamily_go.tsv', sep='\t', index=False, header=False)
    mfo_df.to_csv('mfo_superfamily_go.tsv', sep='\t', index=False, header=False)

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
