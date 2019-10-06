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
    parser.add_argument('-p', '--psiblast_file', help='PSI-BLAST file')
    parser.add_argument('-s', '--structure_file', help='sturcure string file')
    parser.add_argument('-o', '--output_folder', default="slice_results", help='sliced files folder')

    args = parser.parse_args()

    if not os.path.exists(args.psiblast_file):
        print "psiblast_file not found."
        sys.exit(1)

    if not os.path.exists(args.structure_file):
        print "structure_file not found."
        sys.exit(1)

    if not os.path.exists(args.output_folder):
        os.mkdir(args.output_folder)
    if not os.path.exists(args.output_folder + '/c'):
        os.mkdir(args.output_folder + '/c')
    if not os.path.exists(args.output_folder + '/e'):
        os.mkdir(args.output_folder + '/e')
    if not os.path.exists(args.output_folder + '/h'):
        os.mkdir(args.output_folder + '/h')

def main():

    process_options()

    with open(args.psiblast_file, 'r') as f:
        PSSM = f.read().splitlines()
        if len(PSSM) < 4:
            print "psiblast_file format is not correct"
            return None

    with open(args.structure_file, 'r') as f:
        lines = f.readlines()
        if lines[0].startswith("#"):
            del lines[0]

    if len(lines) != 1:
        print len(lines)
        print "structure_file format is not correct"
        return None
    else:
        structure_str = lines[0]

    fragments = re.split('(H+|E+|C+)', structure_str)
    H_list = []
    E_list = []
    C_list = []

    # split structure_str
    ind = 1
    for frag in fragments:
        if len(frag) == 0:
            continue
        else:
            if frag[0] == 'H':
                H_list.append( [ ind, ind+len(frag)-1 ] )
                ind = ind + len(frag)
            elif frag[0] == 'E':
                E_list.append( [ ind, ind+len(frag)-1 ] )
                ind = ind + len(frag)
            elif frag[0] == 'C':
                C_list.append( [ ind, ind+len(frag)-1 ] )
                ind = ind + len(frag)

    structure_list = ['h','e','c']
    frag_position_list = [H_list, E_list, C_list]

    for s, frag_positions in enumerate(frag_position_list):
        for ind, frag_position in enumerate(frag_positions):
            with open('%s/%s/%s%i.txt' % (args.output_folder, structure_list[s], structure_list[s], ind), 'w') as f:
                f.write('\n')
                f.write(PSSM[1])
                f.write('\n')
                f.write(PSSM[2])
                f.write('\n')
                for l in PSSM[frag_position[0]+2:frag_position[1]+3]:
                    f.write(l)
                    f.write('\n')

if __name__ == "__main__":
    main()
