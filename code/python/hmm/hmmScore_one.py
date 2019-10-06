import os
import sys
import pandas
import time
import argparse

global args

def process_options():
    global args

    parser = argparse.ArgumentParser(description='Genarate CAFA2 format score result from hmmscan results.')
    parser.add_argument('-i', '--input_file', help='hmmscan results file')
    parser.add_argument('-o', '--output_file', default='leaf_score.txt', help='CAFA2 format score result')

    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print "input_file not found."
        sys.exit(1)

def main():

    process_options()


    col = ['target', 'target_accession', 'query', 'query_accession', 'f_E-value', 'f_score', 'f_bias',
           'f_E-value', 'f_score', 'f_bias', 'exp', 'reg', 'clu', 'ov', 'env', 'dom', 'rep', 'inc',
           ' description']

    res_df = pandas.read_csv(args.input_file, delim_whitespace=True, comment='#', names=col, engine='python')

    res_df = res_df.loc[:,['query', 'target']]

    res_df = res_df.drop_duplicates().reset_index(drop=True)

    with open(args.output_file, 'w') as f:
        f.write("AUTHOR NCCUCS\n")
        f.write("MODEL 1\n")
        f.write("KEYWORDS\tHMM\n")
        for i in range(0,len(res_df.index)):
            f.write(res_df.loc[i,'query'])
            f.write('\t')
            f.write(res_df.loc[i,'target'])
            f.write('\t')
            f.write('1.00')
            f.write('\n')
        f.write('END')

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
