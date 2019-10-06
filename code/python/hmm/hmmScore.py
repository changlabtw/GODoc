import os
import sys
import pandas
import time
import multiprocessing
import argparse

global args

def process_options():
    global args

    parser = argparse.ArgumentParser(description='Genarate CAFA2 format score result from hmmscan results.')
    parser.add_argument('-i', '--input_folder', help='hmmscan results folder')
    parser.add_argument('-o', '--output_file', default='leaf_score.txt', help='CAFA2 format score result')

    args = parser.parse_args()

    if not os.path.exists(args.input_folder):
        print "input_folder not found."
        sys.exit(1)

def parseRes(result_file):

    score_list = []

    col = ['target', 'target_accession', 'query', 'query_accession', 'f_E-value', 'f_score', 'f_bias',
           'f_E-value', 'f_score', 'f_bias', 'exp', 'reg', 'clu', 'ov', 'env', 'dom', 'rep', 'inc',
           ' description']

    try:
        res_df = pandas.read_csv(result_file, delim_whitespace=True, comment='#', names=col, engine='python')
    except ValueError:
        return score_list

    gos = res_df['target'].unique()

    for go in gos:
        score_str = ("%s\t%s\t%s\n" % (res_df.loc[0,'query'], go, '1.00'))
        score_list.append(score_str)

    # for i in range(0,len(res_df.index)):
    #     score_str = ("%s\t%s\t%s\n" % (res_df.loc[i,'query'], res_df.loc[i,'target'], '1.00'))
    #     score_list.append(score_str)

    return score_list

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

    with open(args.output_file, 'w') as f:
        f.write("AUTHOR NCCUCS\n")
        f.write("MODEL 1\n")
        f.write("KEYWORDS\tHMM\n")
        results = rs.get()
        for rows in results:
            for row in rows:
                f.write(row)
        f.write('END')

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
