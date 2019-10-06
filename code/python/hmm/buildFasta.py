from Bio import SeqIO
import multiprocessing
import argparse
import pandas
import numpy
import time
import sys
import os

global args

def process_options():
    global args

    parser = argparse.ArgumentParser(description='Build fasta file from GO list and function file')
    parser.add_argument('-f', '--fasta_file', help='')
    parser.add_argument('-l', '--label_file', help='')
    parser.add_argument('-g', '--GO_list_file', help='')
    parser.add_argument('-o','--output_folder',help='Output folder name', default='GOFastas')

    args = parser.parse_args()

    if not os.path.exists(args.fasta_file):
        print "fasta_file not found."
        sys.exit(1)

    if not os.path.exists(args.label_file):
        print "label_file not found."
        sys.exit(1)

    if not os.path.exists(args.GO_list_file):
        print "GO_list_file not found."
        sys.exit(1)

    if not os.path.exists(args.output_folder):
        os.mkdir(args.output_folder)

def build_fasta(GO):

    record_dict = SeqIO.index(args.fasta_file, "fasta")
    ID_list = list(record_dict.keys())

    label_df = pandas.read_csv(args.label_file, '\t', names=['ID','GO'])

    IDs = label_df[label_df['GO'] == GO]['ID'].values
    with open('%s/%s.fasta' % (args.output_folder, GO), 'w' ) as f:
        for ind, ID in enumerate(IDs):
            if ID in ID_list:
                SeqIO.write(record_dict[ID], f, 'fasta')
            else:
                print 'There is no %s in %s fasta file.' % (ID, args.fasta_file)

    return None

def build_fasta_helper(args):
    return build_fasta(*args)


def main():

    process_options()

    with open(args.GO_list_file, 'r') as f:
        GO_list = f.read().splitlines()

    build_fasta_args = []
    for GO in GO_list:
        build_fasta_args.append([ GO ])

    p = multiprocessing.Pool()
    rs = p.map_async(build_fasta_helper, build_fasta_args)
    p.close() # No more work
    while (True):
      if (rs.ready()): break
      remaining = rs._number_left
      print "Waiting for", remaining, "tasks to complete..."
      time.sleep(2)

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
