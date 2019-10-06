import os
import sys
import time
import argparse
import numpy

global args

def process_options():
    global args

    parser = argparse.ArgumentParser(description='Merge TFPSSM vectors')
    parser.add_argument('-a', '--helix_folder', help='alpha-helix TFPSSMs folder')
    parser.add_argument('-b', '--sheet_folder', help='beta-sheet TFPSSMs folder')
    parser.add_argument('-c', '--coil_folder', help='coil TFPSSMs folder')
    parser.add_argument('-o', '--output_file', default='stfpssm_vector.csv', help='output file')
    parser.add_argument('-oa', '--helix_output_file', default='helix_stfpssm_vector.csv', help='output file')
    parser.add_argument('-ob', '--sheet_output_file', default='sheet_stfpssm_vector.csv', help='output file')
    parser.add_argument('-oc', '--coil_output_file', default='coil_stfpssm_vector.csv', help='output file')

    args = parser.parse_args()

    if not os.path.exists(args.helix_folder):
        print "helix_folder not found."
        sys.exit(1)

    if not os.path.exists(args.sheet_folder):
        print "sheet_folder not found."
        sys.exit(1)

    if not os.path.exists(args.coil_folder):
        print "coil_folder not found."
        sys.exit(1)

def main():

    process_options()

    h_list = [os.path.join(args.helix_folder, f) for f in os.listdir(args.helix_folder) if os.path.isfile(os.path.join(args.helix_folder, f))]
    e_list = [os.path.join(args.sheet_folder, f) for f in os.listdir(args.sheet_folder) if os.path.isfile(os.path.join(args.sheet_folder, f))]
    c_list = [os.path.join(args.coil_folder, f) for f in os.listdir(args.coil_folder) if os.path.isfile(os.path.join(args.coil_folder, f))]

    all_list = [h_list, e_list, c_list]
    output_files = [args.helix_output_file, args.sheet_output_file, args.coil_output_file]
    vector_d = [13, 5 ,10]

    structure_vector = []
    for ind, path_list in enumerate(all_list):
        cur_structure_vector = []
        valid_count = 0
        for cur_path in path_list:
            with open(cur_path, 'r') as f:
                lines = f.read().splitlines()
                cur_vec = map(float,filter(bool,lines[0].split(',')))
            if len(cur_vec) != 20*(vector_d[ind]+1)*20 or numpy.isnan(numpy.sum(cur_vec)):
                print("vector in %s format isn't correct" % cur_path)
                continue
            else:
                valid_count = valid_count + 1
                if len(cur_structure_vector) == 0:
                    cur_structure_vector = cur_vec
                else:
                    cur_structure_vector = [ x + y for x, y in zip( cur_structure_vector, cur_vec ) ]
        if len(cur_structure_vector) !=0:
            cur_structure_vector = [ x/valid_count for x in cur_structure_vector ]
        else:
            cur_structure_vector = [0.0] * 20*(vector_d[ind]+1)*20
            # print "structure_vector format isn't correct, skip generate vector file"
            # return None
        structure_vector = structure_vector + cur_structure_vector
        with open(output_files[ind], 'w') as f:
            f.write(','.join(map(str,cur_structure_vector)))

    with open(args.output_file, 'w') as f:
        f.write(','.join(map(str,structure_vector)))

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
