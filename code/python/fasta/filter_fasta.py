from Bio import SeqIO
import argparse
import time
import sys
import os

global args

def process_options():
    global args

    parser = argparse.ArgumentParser(description='Filter fasta by ID')
    parser.add_argument('-i', '--fasta_file', help='Fasta file')
    parser.add_argument('-l', '--list_file', help='ID list file')
    parser.add_argument('-o','--output_file',help='Output file name', default='filtered_seq.fasta')

    args = parser.parse_args()

    if not os.path.exists(args.fasta_file):
        print "fasta_file not found."
        sys.exit(1)

    if not os.path.exists(args.list_file):
        print "list_file not found."
        sys.exit(1)

def main():

    process_options()

    record_dict = SeqIO.index(args.fasta_file, "fasta")
    with open(args.list_file, 'r') as f:
        ID_list = f.read().splitlines()

    with open(args.output_file, 'w') as f:
        for ID in ID_list:
            SeqIO.write(record_dict[ID], f, 'fasta')

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
