from Bio import SeqIO
import argparse
import time
import math
import sys
import os

global args

def process_options():
    global args

    parser = argparse.ArgumentParser(description='Split huge fasta file to small fasta files.')
    parser.add_argument('-i', '--fasta_file', help='Target fasta file')
    parser.add_argument('-t', '--type', type=str, default='s', choices=['s','f'], help='Type of batch, s: split, f: fixed')
    parser.add_argument('-n', '--split_num', type=int, default=2)
    parser.add_argument('-a', '--fixed_amount', type=int, default=10000)
    parser.add_argument('-o','--output_folder',help='Output folder name', default='batchs')

    args = parser.parse_args()

    if not os.path.exists(args.fasta_file):
        print "fasta_file not found."
        sys.exit(1)
    if not os.path.exists(args.output_folder):
        os.mkdir(args.output_folder)

def main():

    process_options()

    record_dict = SeqIO.index(args.fasta_file, "fasta")

    ID_list = list(record_dict.keys())

    if args.type == 's':
        per_batch = int(math.ceil((len(ID_list)/float(args.split_num))))
        batch = []
        for i in range(0,args.split_num):
            batch.append( ID_list[ i*per_batch : (i+1) * per_batch ] )
    elif args.type == 'f':
        batch_num = int(math.ceil(len(ID_list)/float(args.fixed_amount)))
        batch = []
        for i in range(0,batch_num):
            batch.append( ID_list[ i * args.fixed_amount : (i+1) * args.fixed_amount ])

    for ind, b in enumerate(batch):
        with open('%s/%s_batch%i.fasta' % (args.output_folder, os.path.basename(args.fasta_file).split('.')[0], ind), 'w') as f:
            for ID in b:
                SeqIO.write(record_dict[ID], f, 'fasta')


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
