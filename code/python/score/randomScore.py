import os
import sys
import pandas
import numpy
import time
import multiprocessing
import random

global pred_res_file
global output_file
global pred_res_df

def process_options(argv = sys.argv):
    global pred_res_file
    global output_file

    if len(argv) < 3:
		print "Usage: %s pred_res_file output_file" % argv[0]
		sys.exit(1)
    elif len(argv) == 3:
        pred_res_file = argv[1]
        output_file = argv[2]

    if not os.path.exists(pred_res_file):
        print "pred_res_file not found."
        sys.exit(1)

def parse(ind):

    gos = pred_res_df.loc[ind,'pred_class'].split(',')
    with open(output_file, 'a') as f:
        for go in gos:
            f.write(pred_res_df.loc[ind, 'ID'] + '\t' + go + '\t' + str(round(random.random(),2)) + '\n')

    return None

def parse_helper(args):
    return parse(*args)

def main():

    global pred_res_df

    process_options()

    with open(output_file, 'w') as f:
        f.write("AUTHOR TEAM_NAME\n")
        f.write("MODEL 1\n")
        f.write("KEYWORDS\tsequence alignment.\n")

    pred_res_df = pandas.read_csv(pred_res_file, sep='\t' ,header=0)

    pool = multiprocessing.Pool()
    parse_args = []

    for i in range(0,len(pred_res_df.index)):
        parse_args.append([i])

    p = multiprocessing.Pool()
    rs = p.map_async(parse_helper, parse_args)
    p.close() # No more work
    while (True):
        if (rs.ready()): break
        remaining = rs._number_left
        print "Waiting for", remaining, "tasks to complete..."
        time.sleep(2)

    with open(output_file, 'a') as f:
        f.write("END\n")

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
