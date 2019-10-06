import os
import sys
import pandas
import time
import argparse

global args

def process_options():
    global args

    parser = argparse.ArgumentParser(description='PCA with nfold')
    parser.add_argument('-i','--vector_file', help='Training vector folder')
    parser.add_argument('-n','--num_fold',help='fold number', type=int, default=5)
    parser.add_argument('-o','--output_folder',help='Output file name', default='nfold_result')

    args = parser.parse_args()

    if not os.path.exists(args.vector_file):
        print "vector_file not found."
        sys.exit(1)

    if not os.path.exists(args.output_folder):
        os.mkdir(args.output_folder)

    if os.listdir(args.output_folder) != []:
        print "output_folder isn't empty."
        sys.exit(1)

def main():

    process_options()

    vector_df = pandas.read_csv(args.vector_file, header=None)
    with open(args.vector_file, 'r') as f:
        lines = f.read().splitlines()

    num_fold = args.num_fold
    for fold in range(0,num_fold):
        train_i = []
        test_i = []
        for i in range(0, len(lines)):
            if i % num_fold != fold:
                train_i.append(i)
            else:
                test_i.append(i)
        cur_output = ("%s/fold%i" % (args.output_folder, fold))
        if not os.path.exists(cur_output):
            os.mkdir(cur_output)
        with open('%s/train_pca.csv' % cur_output,'w') as f:
            for i in train_i:
                f.write(lines[i])
                f.write('\n')
        with open('%s/test_pca.csv' % cur_output,'w') as f:
            for i in test_i:
                f.write(lines[i])
                f.write('\n')

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
