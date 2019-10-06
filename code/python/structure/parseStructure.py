import os
import sys
import time
import argparse
import re

global args

def process_options():
    global args

    parser = argparse.ArgumentParser(description='Parse structure string from horiz file')
    parser.add_argument('-i', '--input_file', help='PSIPRED output horiz file')
    parser.add_argument('-pre', '--preprocess', type=bool, default=True, help='With preprocess or not')
    parser.add_argument('-o', '--output_file', help='structure string', default="")

    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print "input_file not found."
        sys.exit(1)

def main():

    process_options()

    with open(args.input_file, 'r') as f:
        lines = f.readlines()

    structure_str = ""

    for ind, line in enumerate(lines):
        if ind == 0:
            continue
        elif (ind-1) % 6 == 2:
            structure_str += re.split('\W+',line)[1]

    if ( args.preprocess ):
        structure_str = list(structure_str)
        count = 0
        for i in range(1,len(structure_str)-1):
            if structure_str[i-1] == structure_str[i+1] and structure_str[i] != structure_str[i-1]:
                structure_str[i] = structure_str[i-1]
                count = count + 1
        if structure_str[0] != structure_str[1]:
            structure_str[0] = structure_str[1]
        if structure_str[-1] != structure_str[-2]:
            structure_str[-1] = structure_str[-2]
        print float(count)/len(structure_str)
        structure_str = ''.join(structure_str)

    if ( args.output_file == "" ):
        args.output_file = os.path.basename(args.input_file).split('.')[0] + ".txt"

    with open(args.output_file, 'w') as f:
        if ( args.preprocess ):
            f.write('#With preprocess\n')
        f.write(structure_str)


if __name__ == "__main__":
    main()
