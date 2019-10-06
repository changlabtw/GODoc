import os
import sys
import pandas
import time
import argparse
import numpy as np
import multiprocessing

global args

def process_options():
    global args

    parser = argparse.ArgumentParser(description='Merge vector from folder')
    parser.add_argument('-i','--vector_folder', help='Vector folder')
    parser.add_argument('-l','--label_file', help='label file', default="")
    parser.add_argument('-list','--ID_list', action='store_true', help='swich label to ID list file')
    parser.add_argument('-a','--all_files', action='store_true', help='parse whole folder, without using label file')
    parser.add_argument('-o','--output_file',help='Output file name', default='vector.csv')

    args = parser.parse_args()

    if not os.path.exists(args.vector_folder):
        print "vector_folder not found."
        sys.exit(1)

    if not os.path.exists(args.label_file) and args.all_files!=True:
        print "label_file not found."
        sys.exit(1)

def load_vector(ID):

    cur_vector = []
    with open(args.vector_folder + ID + '.txt', 'r') as f:
        lines = f.read().splitlines()
        if len(lines) != 1:
            print "Skip " + ID + ".txt"
            return None
        else:
            cur_list = lines[0].split(',')
            if (cur_list[-1] == ''):
                cur_vector = map(float,(cur_list[:-1]))
            else:
                cur_vector = map(float,(cur_list))
        vector_sum = np.sum(cur_vector)
        if np.isnan(vector_sum) or vector_sum == 0:
            return None

    return [ID, cur_vector]

def load_vector_helper(args):
    return load_vector(*args)

def main():

    process_options()

    if args.all_files:
        file_name_list = [ f for f in os.listdir(args.vector_folder) if os.path.isfile(os.path.join(args.vector_folder, f))]
        ID_list = [ file_name.split('.')[0] for file_name in file_name_list]
    else:
        if args.ID_list:
            ID_df = pandas.read_csv(args.label_file, sep='\t', names=['ID'])
            ID_list = ID_df['ID'].unique()
        else:
            label_df = pandas.read_csv(args.label_file, sep='\t', names=['ID', 'GO'])
            ID_list = label_df['ID'].unique()

    load_vector_args = []

    for ID in ID_list:
        if not os.path.exists(args.vector_folder + ID + '.txt'):
            print "Skip " + ID + ".txt"
        else:
            load_vector_args.append([ID])

    p = multiprocessing.Pool()
    rs = p.map_async(load_vector_helper, load_vector_args)
    p.close() # No more work
    while (True):
      if (rs.ready()): break
      remaining = rs._number_left
      print "Waiting for", remaining, "tasks to complete..."
      time.sleep(2)

    train_ID = []
    train_data = []

    with open(args.output_file,'w') as f:
        results = rs.get()
        for row in results:
            if row == None:
                continue
            else:
                f.write(row[0])
                f.write(',')
                f.write(','.join([str(val) for val in row[1]]))
                f.write('\n')

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
