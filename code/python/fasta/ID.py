from Bio import SeqIO
import argparse
import time
import sys
import os

global args

def process_options():
    global args

    parser = argparse.ArgumentParser(description='Output fasta IDs')
    parser.add_argument('-f', '--fasta_file', help='Fasta file')
    parser.add_argument('-o','--output_file',help='Output file name', default='fasta_ID.txt')

    args = parser.parse_args()

    if not os.path.exists(args.fasta_file):
        print "fasta_file not found."
        sys.exit(1)

def main():

    process_options()

    record_dict = SeqIO.index(args.fasta_file, "fasta")
    ID_list = list(record_dict.keys())

    with open(args.output_file, 'w') as f:
        for ID in ID_list:
            f.write("%s\n" % ID)

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
