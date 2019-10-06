import os
import sys
import pandas
import time
import multiprocessing
import argparse

global args

def process_options():
    global args

    parser = argparse.ArgumentParser(description='Get means from fragment analysis files')
    parser.add_argument('-i', '--input_folder', help='hmmscan results folder')

    args = parser.parse_args()

    if not os.path.exists(args.input_folder):
        print "input_folder not found."
        sys.exit(1)

def parseRes(result_file):

    score_list = []

    with open(result_file, 'r') as f:
        lines = f.read().splitlines()

    return map(float,lines[1].split(','))

def parseRes_helper(args):
    return parseRes(*args)

def main():

    process_options()

    file_list = [os.path.join(args.input_folder, f) for f in os.listdir(args.input_folder) if os.path.isfile(os.path.join(args.input_folder, f))]

    parseRes_args = []
    for file_path in file_list:
        parseRes_args.append([file_path])

    pool = multiprocessing.Pool()
    p = multiprocessing.Pool()
    rs = p.map_async(parseRes_helper, parseRes_args)
    p.close() # No more work
    while (True):
      if (rs.ready()): break
      remaining = rs._number_left
      print "Waiting for", remaining, "tasks to complete..."
      time.sleep(2)

    results = rs.get()
    with open(file_list[0], 'r') as f:
        lines = f.read().splitlines()
        col = lines[0].split(',')
    res_df = pandas.DataFrame(columns=col)
    for ind, row in enumerate(results):
        res_df.loc[ind] = row

    print res_df.describe().loc['mean',:]

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
