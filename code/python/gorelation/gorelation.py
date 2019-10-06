import os
import sys
import time
import pandas
import argparse
import multiprocessing

global function_df

def process_options(argv = sys.argv):
    global args

    parser = argparse.ArgumentParser(description='Get GO relation')
    parser.add_argument('-i', '--function_file', help='GO annotaion file')
    parser.add_argument('-t', '--threshold', help='frequence threshold', default=0.1)
    parser.add_argument('-o','--output_file',help='Output file name', default='GO_relation.tsv')

    args = parser.parse_args()

    if not os.path.exists(args.function_file):
        print "function_file not found."
        sys.exit(1)

    if os.path.exists(args.output_file):
        print "output_file already exists."
        sys.exit(1)

def query(go, threshold):

    global function_df

    current_IDs = function_df[function_df['GO'] == go]['ID']
    sta_df = function_df[function_df['ID'].isin(current_IDs)].groupby(['GO']).count().sort_values(['ID'],ascending=False)
    sta_df['freq'] = sta_df['ID'] / float(sta_df['ID'].max())
    sta_df = sta_df[(sta_df['freq'] >= args.threshold) & (sta_df['freq'] != 1.0)].reset_index()
    cur_rel = ''
    if len(sta_df) != 0 :
        for i in range(0,len(sta_df)):
            cur_rel = cur_rel + sta_df.loc[i,['GO']].values[0] + ',' + str(sta_df.loc[i,['freq']].values[0]) + ';'
        return [go, cur_rel]
    else:
        return []

def query_helper(args):
    return query(*args)

def main():

    global function_df

    process_options()

    function_df = pandas.read_csv(args.function_file, sep='\t', names=['ID','GO'])
    res_df = pandas.DataFrame(columns=['GO','rel'])
    go_list = function_df['GO'].unique()

    query_args = []

    for go in go_list:
        query_args.append([go, args.threshold])

    pool = multiprocessing.Pool()
    p = multiprocessing.Pool()
    rs = p.map_async(query_helper, query_args)
    p.close() # No more work
    while (True):
      if (rs.ready()): break
      remaining = rs._number_left
      print "Waiting for", remaining, "tasks to complete..."
      time.sleep(2)

    results = rs.get()
    results = filter(lambda x:len(x) != 0, results)

    for ind,row in enumerate(results):
        res_df.loc[ind] = row

    res_df.to_csv(args.output_file, sep='\t', index=False)

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
