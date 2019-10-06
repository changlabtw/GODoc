import os
import sys
import time
import argparse
import re
import editdistance

global args

def process_options():
    global args

    parser = argparse.ArgumentParser(description='Compare structure string edit distance with two horiz file.')
    parser.add_argument('-a', '--horiz_a', help='')
    parser.add_argument('-b', '--horiz_b', help='')

    args = parser.parse_args()

    if not os.path.exists(args.horiz_a):
        print "horiz_a not found."
        sys.exit(1)

    if not os.path.exists(args.horiz_b):
        print "horiz_b not found."
        sys.exit(1)

def main():

    process_options()

    with open(args.horiz_a, 'r') as f:
        lines_a = f.readlines()

    with open(args.horiz_b, 'r') as f:
        lines_b = f.readlines()

    if len(lines_a) == 1:
        print "horiz_a format isn't correct"
        quit()
    elif len(lines_b) == 1:
        print "horiz_b format isn't correct"
        quit()

    horiz_a = ""
    horiz_b = ""

    for ind, line in enumerate(lines_a):
        if ind == 0:
            continue
        elif (ind-1) % 6 == 2:
            horiz_a += re.split('\W+',line)[1]

    for ind, line in enumerate(lines_b):
        if ind == 0:
            continue
        elif (ind-1) % 6 == 2:
            horiz_b += re.split('\W+',line)[1]

    if len(horiz_a) != len(horiz_b):
        print "Length are not equal, cannot compare."
    else:
        print format(float(editdistance.eval(horiz_a, horiz_b))/len(horiz_a),'.2f')


if __name__ == "__main__":
    main()
