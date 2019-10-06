from Bio import SeqIO
import argparse
import random
import time
import sys
import os

global args

def process_options():
    global args

    parser = argparse.ArgumentParser(description='Split ID list to nfold.')
    parser.add_argument('-i', '--list_file', help='ID list file')
    parser.add_argument('-n', '--n', help='fold amount', type=int, default=5)
    parser.add_argument('-o','--output',help='Output folder', default='nfold')

    args = parser.parse_args()

    if not os.path.exists(args.list_file):
        print "list_file not found."
        sys.exit(1)

    if not os.path.exists(args.output):
        os.mkdir(args.output)

def main():

    process_options()

    with open(args.list_file, 'r') as f:
        ID_list = f.read().splitlines()

    random.shuffle(ID_list)

    folds = [ [] for i in range(0,args.n)]

    for ind, ID in enumerate(ID_list):
        folds[ind%args.n].append(ID)

    for ind, fold in enumerate(folds):
        cur_fold = args.output+'/fold'+str(ind)+'/'
        if not os.path.exists(cur_fold):
            os.mkdir(cur_fold)
        cur_train_ID = [ f for i, f in enumerate(folds) if i!=ind ]
        cur_train_ID = [ ele for sub in cur_train_ID for ele in sub]
        with open(cur_fold+'test_ID.txt', 'w') as f:
            f.write('\n'.join(fold))
            f.write('\n')
        with open(cur_fold+'train_ID.txt', 'w') as f:
            f.write('\n'.join(cur_train_ID))
            f.write('\n')

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
