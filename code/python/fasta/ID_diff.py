import argparse
import numpy
import time
import sys
import os

global args

def process_options():
    global args

    parser = argparse.ArgumentParser(description='a-b')
    parser.add_argument('-a', '--a_file', help='ID file')
    parser.add_argument('-b', '--b_file', help='ID file')
    parser.add_argument('-o','--output_file',help='Output file name', default='fasta_ID.txt')

    args = parser.parse_args()

    if not os.path.exists(args.a_file):
        print "a_file not found."
        sys.exit(1)

    if not os.path.exists(args.b_file):
        print "b_file not found."
        sys.exit(1)

def main():

    process_options()

    with open(args.a_file, 'r') as f:
        a = f.read().splitlines()

    with open(args.b_file, 'r') as f:
        b = f.read().splitlines()

    c = numpy.setdiff1d(a,b)

    with open(args.output_file, 'w') as f:
        for ID in c:
            f.write("%s\n" % ID)

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
