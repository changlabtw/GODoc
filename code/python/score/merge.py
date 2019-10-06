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
    parser.add_argument('-a','--a_file', help='CAFA2 format output file')
    parser.add_argument('-b','--b_file', help='CAFA2 format output file')
    parser.add_argument('-o','--output_file',help='Output file name', default='merge_score.txt')

    args = parser.parse_args()

    if not os.path.exists(args.a_file):
        print "a_file not found."
        sys.exit(1)

    if not os.path.exists(args.b_file):
        print "b_file not found."
        sys.exit(1)

def main():

    process_options()

    a_df = pandas.read_csv(args.a_file, sep='\t', names=['ID', 'GO', 'score'], skiprows=3, skipfooter=1 ,engine='python')
    b_df = pandas.read_csv(args.b_file, sep='\t', names=['ID', 'GO', 'score'], skiprows=3, skipfooter=1 ,engine='python')

    ID_list = np.union1d(a_df['ID'].unique(),b_df['ID'].unique())

    with open(args.output_file, 'w') as f:
        f.write('AUTHOR NCCUCS\n')
        f.write('MODEL 1\n')
        f.write('KEYWORDS\tHMM+TFPSSM\n')
        for ID in ID_list:
            cur_a_gos = a_df[a_df['ID'] == ID]['GO'].values
            cur_b_gos = b_df[b_df['ID'] == ID]['GO'].values
            cur_gos = np.union1d(cur_a_gos, cur_b_gos)
            # cur_gos = np.intersect1d(cur_a_gos, cur_b_gos)
            # cur_gos = np.setdiff1d(cur_a_gos, cur_b_gos)
            for go in cur_gos:
                f.write('%s\t%s\t%s\n' % (ID, go, '1.00'))
        f.write('END\n')

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
