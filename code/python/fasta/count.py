import os
import sys
import time
from Bio import SeqIO

global fasta_file

def process_options(argv = sys.argv):
    global fasta_file

    if len(argv) < 2:
		print "Usage: %s fasta_file" % argv[0]
		sys.exit(1)

    fasta_file = argv[1]

    if not os.path.exists(fasta_file):
        print "fasta_file not found."
        sys.exit(1)

def main():

    process_options()

    record_dict = SeqIO.index(fasta_file, "fasta")

    print len(record_dict)


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
