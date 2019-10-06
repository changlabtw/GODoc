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
    parser.add_argument('-t', '--type', help='type of threshold', type=str, choices=['k','e'], required=True)
    parser.add_argument('-k', '--k', help='top k', type=int)
    parser.add_argument('-e', '--e', help='E-value threshold', type=int)
    parser.add_argument('-o', '--output_file', default='leaf_score.txt', help='CAFA2 format score result')

    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print "input_file not found."
        sys.exit(1)

def main():

    process_options()


    col = ['target', 'target_accession', 'query', 'query_accession', 'f_E-value', 'f_score', 'f_bias',
           'b_E-value', 'b_score', 'b_bias', 'exp', 'reg', 'clu', 'ov', 'env', 'dom', 'rep', 'inc',
           ' description']

    res_df = pandas.read_csv(args.input_file, delim_whitespace=True, comment='#', names=col, engine='python')

    # res_df = res_df[ (res_df['b_E-value'] < 1e-5) & (res_df['b_score'] >= 37.8) ]
    #res_df = res_df[ (res_df['b_E-value'] < 1e-5)]
    #max_b_score = res_df['b_score'].max()

    if(args.type == 'k'):
        query_list = res_df['query'].unique()
        k = args.k
    elif(args.type == 'e'):
        res_df = res_df[ (res_df['b_E-value'] < 10**args.e)]

    res_df = res_df.loc[:,['query', 'target', 'b_score']]
    res_df = res_df.drop_duplicates(['query', 'target']).reset_index(drop=True)

    with open(args.output_file, 'w') as f:
        f.write("AUTHOR NCCUCS\n")
        f.write("MODEL 1\n")
        f.write("KEYWORDS\tHMM\n")
        if(args.type == 'k'):
            for query in query_list:
                cur_df = res_df[res_df['query'] == query].iloc[0:k].reset_index(drop=True)
                for i in range(0,len(cur_df.index)):
                    f.write(cur_df.loc[i,'query'])
                    f.write('\t')
                    f.write(cur_df.loc[i,'target'])
                    f.write('\t')
                    f.write('1.00')
                    f.write('\n')
        elif(args.type == 'e'):
            for i in range(0,len(res_df.index)):
                f.write(res_df.loc[i,'query'])
                f.write('\t')
                f.write(res_df.loc[i,'target'])
                f.write('\t')
                f.write('1.00')
                # f.write(format(round(res_df.loc[i,'b_score']/max_b_score,2),'.2f'))
                f.write('\n')
        f.write('END')

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
