import os
import sys
import time
import argparse
import pandas
import numpy

global args

def process_options():
    global args

    parser = argparse.ArgumentParser(description='Merge TFPSSM vectors')
    parser.add_argument('-a', '--file_a', help='vectors file a')
    parser.add_argument('-b', '--file_b', help='vectors file b')
    parser.add_argument('-o', '--output_file', default='all_vector.csv', help='output file')

    args = parser.parse_args()

    if not os.path.exists(args.file_a):
        print "file_a not found."
        sys.exit(1)

    if not os.path.exists(args.file_b):
        print "file_b not found."
        sys.exit(1)

def main():

    process_options()

    a_df = pandas.read_csv(args.file_a, header=None)
    b_df = pandas.read_csv(args.file_b, header=None)

    a_ID = a_df.loc[:,0]
    b_ID = b_df.loc[:,0]

    ID_list = numpy.intersect1d(a_ID,b_ID)

    print ID_list

    with open(args.output_file, 'w') as f:
        for ID in ID_list:
            cur_vec = list(a_df[a_df[0]==ID].loc[:,1:].values[0]) + list(b_df[b_df[0]==ID].loc[:,1:].values[0])
            f.write(ID)
            f.write(',')
            f.write(','.join(map(str,cur_vec)))
            f.write('\n')

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
