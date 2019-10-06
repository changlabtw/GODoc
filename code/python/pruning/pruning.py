import os
import sys
import pandas
import time
import argparse

global args

def process_options():
    global args

    parser = argparse.ArgumentParser(description='Get FP/TP ratio')
    parser.add_argument('-i','--input',help='Score file')
    parser.add_argument('-r','--ratio_file',help='GO ratio file')
    parser.add_argument('-t','--threshold',help='Ration threshold', type=float, default=0.01)
    parser.add_argument('-o','--output',help='Output file name', default='pruning_res.txt')

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print "pred_file not found."
        sys.exit(1)

    if not os.path.exists(args.ratio_file):
        print "ratio_file not found."
        sys.exit(1)

    if os.path.exists(args.output):
        print "output allready exists."
        sys.exit(1)

def main():

    process_options()

    pred_res_df = pandas.read_csv(args.input, engine='python', sep='\t', skip_footer=1, skiprows=3, names=['ID','GO','score'])
    ratio_df = pandas.read_csv(args.ratio_file, sep='\t', converters={'GO':str, 'ratio':float})
    retained_list = list(ratio_df[ ratio_df['ratio'] <= (1-args.threshold)/args.threshold ]['GO'].values)
    pred_res_df = pred_res_df[pred_res_df['GO'].isin(retained_list)].reset_index(drop=True)

    with open(args.output, 'w') as f:
        f.write("AUTHOR TEAM_NAME\n")
        f.write("MODEL 1\n")
        f.write("KEYWORDS\tpruning\n")
        for i in range(0,len(pred_res_df)):
            f.write(pred_res_df.loc[i,'ID'])
            f.write('\t')
            f.write(pred_res_df.loc[i,'GO'])
            f.write('\t')
            f.write(str(pred_res_df.loc[i,'score']))
            f.write('\n')
        f.write("END\n")

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
