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
    parser.add_argument('-g', '--sf_go', help='superfamily to go map')
    parser.add_argument('-k', '--k', help='top k', type=int)
    parser.add_argument('-o','--output',help='Output file name', default='res.txt')

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print "hmm result not found."
        sys.exit(1)

    if not os.path.exists(args.md_sf):
        print "model to family map file not found."
        sys.exit(1)

    if not os.path.exists(args.sf_go):
        print "superfamily to go map file not found."
        sys.exit(1)

    if os.path.exists(args.output):
        print "output allready exists."
        sys.exit(1)

def go_pred(query):
    root = {'P':'GO:0008150','C':'GO:0003674','F':'GO:0005575'}

    res = []
    cur_models = res_df[res_df['query'] == query].sort_values('b_E-value')[0:args.k]['target'].values
    cur_models = [ model.split('|')[-1].split('/')[0] for model in cur_models ]
    cur_sf = md_sf_df[md_sf_df['model'].isin(cur_models)]['sf'].unique()

    try:
        for sf in cur_sf:
            cur_df = sf_go_df[sf_go_df['sf'] == sf]
            if len(cur_df) > 3:
                cur_df['score'] = None
                for cur_type in ['P','C','F']:
                    if len(cur_df[cur_df['type']==cur_type]) > 0:
                        cur_max = cur_df[cur_df['GO']==root[cur_type]]['value'].values[0]
                        cur_df.loc[cur_df['type']==cur_type,'score'] = cur_df[(cur_df['type']==cur_type)]['value'].apply(lambda x: x/float(cur_max))
                cur_df = cur_df.reset_index(drop=True)
                for i in range(0,len(cur_df)):
                    if cur_df.loc[i,'score'] != 1:
                        # res.append([query,cur_df.loc[i,'GO'],cur_df.loc[i,'score']])
                        res.append([query,cur_df.loc[i,'GO'],1.00])
            else:
                print "error"
    except IndexError:
        print cur_df
        print sf

    return res

def go_pred_helper(args):
    return go_pred(*args)

def main():

    global res_df
    global md_sf_df
    global sf_go_df

    process_options()

    col = ['target', 'target_accession', 'query', 'query_accession', 'f_E-value', 'f_score', 'f_bias',
           'b_E-value', 'b_score', 'b_bias', 'exp', 'reg', 'clu', 'ov', 'env', 'dom', 'rep', 'inc',
           ' description']

    res_df = pandas.read_csv(args.input, delim_whitespace=True, comment='#', names=col, engine='python')
    md_sf_df = pandas.read_csv(args.md_sf, names=['model','sf','name','domain'])
    sf_go_df = pandas.read_csv(args.sf_go, sep='\t', names=['sf','GO','type','value'])

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
        f.write("AUTHOR NCCUCS\n")
        f.write("MODEL 1\n")
        f.write("KEYWORDS\tCATH\n")
        results = rs.get()
        for rows in results:
            for row in rows:
                f.write(row[0])
                f.write('\t')
                f.write(row[1])
                f.write('\t')
                f.write(str(row[2]))
                f.write('\n')
        f.write('END')

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
