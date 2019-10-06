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
    parser.add_argument('-a', '--helix_file', help='alpha-helix vectors file')
    parser.add_argument('-b', '--sheet_file', help='beta-sheet vectors file')
    parser.add_argument('-c', '--coil_file', help='coil vectors file')
    parser.add_argument('-o', '--output_file', default='all_vector.csv', help='output file')

    args = parser.parse_args()

    if not os.path.exists(args.helix_file):
        print "helix_file not found."
        sys.exit(1)

    if not os.path.exists(args.sheet_file):
        print "sheet_file not found."
        sys.exit(1)

    if not os.path.exists(args.coil_file):
        print "coil_file not found."
        sys.exit(1)

def main():

    process_options()

    h_df = pandas.read_csv(args.helix_file, header=None)
    e_df = pandas.read_csv(args.sheet_file, header=None)
    c_df = pandas.read_csv(args.coil_file, header=None)

    h_ID = h_df.loc[:,0]
    e_ID = e_df.loc[:,0]
    c_ID = c_df.loc[:,0]

    ID_list = numpy.intersect1d(h_ID,e_ID)
    ID_list = numpy.intersect1d(ID_list,c_ID)

    print ID_list

    with open(args.output_file, 'w') as f:
        for ID in ID_list:
            cur_vec = list(h_df[h_df[0]==ID].loc[:,1:].values[0]) + list(e_df[e_df[0]==ID].loc[:,1:].values[0]) + list(c_df[c_df[0]==ID].loc[:,1:].values[0])
            f.write(ID)
            f.write(',')
            f.write(','.join(map(str,cur_vec)))
            f.write('\n')

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
