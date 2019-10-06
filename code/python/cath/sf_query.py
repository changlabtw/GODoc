import os
import sys
import pandas
import time
import argparse
import multiprocessing

global args
global res_df
global md_sf_df
global sf_go_df

def process_options():
    global args

    parser = argparse.ArgumentParser(description='Get superfamily and GO mapping table from cath.')
    parser.add_argument('-i', '--input', help='hmm result')
    parser.add_argument('-m', '--md_sf', help='model to family map')
    parser.add_argument('-o','--output',help='Output file name', default='ID_sf_map.txt')

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print "hmm result not found."
        sys.exit(1)

    if not os.path.exists(args.md_sf):
        print "model to family map file not found."
        sys.exit(1)

    if os.path.exists(args.output):
        print "output allready exists."
        sys.exit(1)

def go_pred(query):
    root = {'P':'GO:0008150','C':'GO:0003674','F':'GO:0005575'}

    res = []
    cur_models = res_df[res_df['query'] == query].sort_values('b_E-value')[0:1]['target'].values
    cur_models = [ model.split('|')[-1].split('/')[0] for model in cur_models ]
    cur_sf = md_sf_df[md_sf_df['model'].isin(cur_models)]['sf'].unique()

    return [query, cur_sf[0]]

def go_pred_helper(args):
    return go_pred(*args)

def main():

    global res_df
    global md_sf_df

    process_options()

    col = ['target', 'target_accession', 'query', 'query_accession', 'f_E-value', 'f_score', 'f_bias',
           'b_E-value', 'b_score', 'b_bias', 'exp', 'reg', 'clu', 'ov', 'env', 'dom', 'rep', 'inc',
           ' description']

    res_df = pandas.read_csv(args.input, delim_whitespace=True, comment='#', names=col, engine='python')
    md_sf_df = pandas.read_csv(args.md_sf, names=['model','sf','name','domain'])

    query_list = res_df['query'].unique()


    go_pred_args = []
    for query in query_list:
        go_pred_args.append([query])

    pool = multiprocessing.Pool()
    p = multiprocessing.Pool()
    rs = p.map_async(go_pred_helper, go_pred_args)
    p.close() # No more work
    while (True):
      if (rs.ready()): break
      remaining = rs._number_left
      print "Waiting for", remaining, "tasks to complete..."
      time.sleep(2)

    with open(args.output, 'w') as f:
        results = rs.get()
        for row in results:
            f.write(row[0])
            f.write('\t')
            f.write(row[1])
            f.write('\n')

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
