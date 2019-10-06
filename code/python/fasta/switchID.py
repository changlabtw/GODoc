from Bio import SeqIO
import argparse
import time
import sys
import os

global args

def process_options():
    global args

    parser = argparse.ArgumentParser(description='Switch fasta ID for CAFA2 SWISS training data')
    parser.add_argument('-f', '--fasta_file', help='Fasta file')
    parser.add_argument('-l', '--list_file', help='ID pair file')
    parser.add_argument('-o','--output_file',help='Output file name', default='switch.fasta')

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
    pair_list = []

    with open(args.list_file, 'r') as f:
        list_file = f.read().splitlines()

    for line in list_file:
        pair_list.append(line.split('\t'))

    ID_list = list(record_dict.keys())

    with open(args.output_file, 'w') as f:
        for pair in pair_list:
            current = record_dict[pair[1]]
            current.id = pair[0]
            SeqIO.write(current, f, 'fasta')

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
