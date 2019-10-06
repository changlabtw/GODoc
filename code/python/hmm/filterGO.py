import os
import sys
import time
import pandas
import argparse

global args

def process_options(argv = sys.argv):
    global args

    parser = argparse.ArgumentParser(description='Filter GO from funciton tsv file by percent or amount')
    parser.add_argument('-i', '--function_file', help='function tsv file, [ "ID", "GO" ]')
    parser.add_argument('-t', '--type', type=str, choices=['p','a'], default='p', help='p: percent, i: amount')
    parser.add_argument('-p', '--percent', type=float, default=0.68, help='percent threshold')
    parser.add_argument('-a', '--amount', type=int, default=100, help='amout threshold')
    parser.add_argument('-o','--output_file',help='Output file name', default='GO_list.txt')

    args = parser.parse_args()

    if not os.path.exists(args.function_file):
        print "function_file not found."
        sys.exit(1)

def main():

    process_options()

    function_df = pandas.read_csv(args.function_file, sep='\t', names=['ID','GO'])

    sta_go = function_df.groupby('GO').count().sort_values(['ID'],ascending=False)
    sta_go = sta_go.reset_index()

    if args.type == 'a':
        GO_list = sta_go[sta_go['ID']>args.amount]['GO'].values
        print sta_go[sta_go['ID']>args.amount]
    elif args.type == 'p':
        sta_go['freq'] = sta_go['ID'] / float(len(function_df.index))
        sta_go['cum'] = 0
        bound = args.percent
        bound_index = 0
        current_bound = 0
        found = False
        for i in range(0,len(sta_go.index)):
            if i == 0:
                sta_go.loc[i,'cum'] = sta_go.loc[i,'freq']
            else:
                sta_go.loc[i,'cum'] = sta_go.loc[i,'freq'] + sta_go.loc[i-1,'cum']
                if sta_go.loc[i-1,'cum'] < bound and sta_go.loc[i,'cum'] > bound:
                    found = True
                if found:
                    if sta_go.loc[i-1,'ID'] != sta_go.loc[i,'ID']:
                        print "%i is at %f, count=%i." % (i,bound,sta_go.loc[i,'ID'])
                        bound_index = i+1
                        break
        GO_list = sta_go['GO'][0:bound_index].values
        print sta_go.loc[0:bound_index-1,:]

    with open(args.output_file, 'w') as f:
        for GO in GO_list:
            f.write('%s\n' % GO)

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
