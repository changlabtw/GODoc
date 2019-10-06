import argparse
import pandas
import time
import sys
import os

global args

def process_options():
    global args

    parser = argparse.ArgumentParser(description='Filter fasta by ID')
    parser.add_argument('-i', '--label_file', help='label file')
    parser.add_argument('-l', '--list_file', help='ID list file')
    parser.add_argument('-o','--output_file',help='Output file name', default='filtered_label.tsv')

    args = parser.parse_args()

    if not os.path.exists(args.label_file):
        print "label_file not found."
        sys.exit(1)

    if not os.path.exists(args.list_file):
        print "list_file not found."
        sys.exit(1)

def main():

    process_options()

    df = pandas.read_csv(args.label_file, sep='\t', names=['ID','GO'])
    with open(args.list_file, 'r') as f:
        ID_list = f.read().splitlines()

    df = df[df['ID'].isin(ID_list)]
    df.to_csv(args.output_file, sep='\t', index=False, header=False)


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
