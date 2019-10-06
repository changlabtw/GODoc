import os
import sys
import time
import argparse
import multiprocessing
import operator
from Bio import SeqIO
from propy.PyPro import GetProDes

global args

def process_options():
    global args

    parser = argparse.ArgumentParser(description='Get propy CTD features.')
    parser.add_argument('-i', '--input_file', help='fasta file')
    parser.add_argument('-o','--output',help='Output folder name', default='ctd')

    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print "input_file not found."
        sys.exit(1)

    if not os.path.exists(args.output):
        os.mkdir(args.output)

def getCTD(ID, seq):

    des = GetProDes(seq)
    ctd = des.GetCTD()
    ctd = sorted(ctd.items(), key=operator.itemgetter(0)) # sort features by feature names
    ctd = [ str(pair[1]) for pair in ctd ]

    return [ID,ctd]

def getCTD_helper(args):
    return getCTD(*args)

def main():

    process_options()

    record_dict = SeqIO.index(args.input_file, "fasta")
    ID_list = [ key for key in record_dict.keys()]

    getCTD_args = []
    for ID in ID_list:
        getCTD_args.append([ID, str(record_dict[ID].seq)])

    pool = multiprocessing.Pool()
    p = multiprocessing.Pool()
    rs = p.map_async(getCTD_helper, getCTD_args)
    p.close() # No more work
    while (True):
      if (rs.ready()): break
      remaining = rs._number_left
      print "Waiting for", remaining, "tasks to complete..."
      time.sleep(2)

    results = rs.get()
    for res in results:
        with open(args.output+'/'+res[0]+'.txt', 'w') as f:
            f.write(','.join(res[1]))
            f.write('\n')

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
