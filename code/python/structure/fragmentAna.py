import re
import os
import sys
import time
import pandas
import argparse

global args

def process_options():
    global args

    parser = argparse.ArgumentParser(description='Analyze structure')
    parser.add_argument('-i', '--input_file', help='sturcure string file')
    parser.add_argument('-o', '--output_file', default="", help='PSIPRED output horiz file')

    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print "input_file not found."
        sys.exit(1)

def main():

    process_options()

    with open(args.input_file, 'r') as f:
        lines = f.readlines()
        if lines[0].startswith("#"):
            del lines[0]

    if len(lines) != 1:
        print len(lines)
        print "input_file format is not correct"
        sys.exit(1)
    else:
        structure_str = lines[0]

    fragments = re.split('(H+|E+|C+)', structure_str)
    H_list = []
    E_list = []
    C_list = []

    for frag in fragments:
        if len(frag) == 0:
            continue
        else:
            if frag[0] == 'H':
                H_list.append(len(frag))
            elif frag[0] == 'E':
                E_list.append(len(frag))
            elif frag[0] == 'C':
                C_list.append(len(frag))

    des = [pandas.Series(H_list).describe(),pandas.Series(E_list).describe(),pandas.Series(C_list).describe()]
    # print 'H'
    # print 'Lenght:'
    # print des[0]
    # print 'E'
    # print 'Lenght:'
    # print des[1]
    # print 'C'
    # print 'Lenght:'
    # print des[2]

    if (args.output_file == ""):
        args.output_file = os.path.basename(args.input_file).split('.')[0] + "_ana.txt"


    with open(args.output_file, 'w') as f:
        f.write('H_amount,H_mean,H_std,H_min,H_25,H_50,H_75,H_max,'+
                'E_amount,E_mean,E_std,E_min,E_25,E_50,E_75,E_max,'+
                'C_amount,C_mean,C_std,C_min,C_25,C_50,C_75,C_max\n')
        numbers = []
        for d in des:
            numbers.append(d['count'])
            numbers.append(d['mean'])
            numbers.append(d['std'])
            numbers.append(d['min'])
            numbers.append(d['25%'])
            numbers.append(d['50%'])
            numbers.append(d['75%'])
            numbers.append(d['max'])
        f.write(','.join(map(str,numbers)))

if __name__ == "__main__":
    main()
