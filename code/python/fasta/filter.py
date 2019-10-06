from Bio import SeqIO
import argparse
import numpy
import time
import sys
import os

global args

def process_options():
    global args

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-a', '--fasta_a', help='')
    parser.add_argument('-b', '--fasta_b', help='')
    parser.add_argument('-opr', '--operator', type=str, choices=['d','i','u'], default='d', help='d: Set difference, i: intersection, u: union')
    parser.add_argument('-o','--output_file',help='Output file name', default='result.fasta')

    args = parser.parse_args()

    if not os.path.exists(args.fasta_a):
        print "fasta_a not found."
        sys.exit(1)

    if not os.path.exists(args.fasta_b):
        print "fasta_b not found."
        sys.exit(1)

def main():

    process_options()

    fasta_a = args.fasta_a
    fasta_b = args.fasta_b

    record_dict_a = SeqIO.index(fasta_a, "fasta")
    record_dict_b = SeqIO.index(fasta_b, "fasta")

    ID_list_a = list(record_dict_a.keys())
    ID_list_b = list(record_dict_b.keys())

    if args.operator == 'd':
        ID_list_res = numpy.setdiff1d(ID_list_a,ID_list_b)
    elif args.operator == 'i':
        ID_list_res = numpy.intersect1d(ID_list_a,ID_list_b)
    elif args.operator == 'u':
        ID_list_res = numpy.union1d(ID_list_a,ID_list_b)

    with open(args.output_file, 'w') as f:
        if args.operator == 'd':
            for ID in ID_list_res:
                SeqIO.write(record_dict_a[ID], f, 'fasta')
        elif args.operator == 'i':
            for ID in ID_list_res:
                SeqIO.write(record_dict_a[ID], f, 'fasta')
        elif args.operator == 'u':
            for ID in ID_list_a:
                SeqIO.write(record_dict_a[ID], f, 'fasta')
            ID_list_res = numpy.setdiff1d(ID_list_b,ID_list_a)
            for ID in ID_list_res:
                SeqIO.write(record_dict_b[ID], f, 'fasta')


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
