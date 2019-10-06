import os
import sys
import pandas
import time
import multiprocessing
import argparse

global args

def process_options():
    global args

    parser = argparse.ArgumentParser(description='Get FP/TP ratio')
    parser.add_argument('-i','--input',help='Score file')
    parser.add_argument('-l','--testing_label_file',help='Testing label file')
    parser.add_argument('-t','--target_list',help='Target ID list file')
    parser.add_argument('-o','--output',help='Output file name', default='go_ratio.tsv')

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print "train_vec_file not found."
        sys.exit(1)

    if not os.path.exists(args.testing_label_file):
        print "testing_label_file not found."
        sys.exit(1)

    if not os.path.exists(args.target_list):
        print "target_list not found."
        sys.exit(1)

    if os.path.exists(args.output):
        print "output allready exists."
        sys.exit(1)

def query(ind):

    cur_ID = pred_res_df.loc[ind,'ID']
    cur_GO = pred_res_df.loc[ind,'GO']
    gt_list = label_df[label_df['ID'] == cur_ID].values
    if any(cur_GO in gt for gt in gt_list):
        cur_label = "TP"
    else:
        cur_label = "FP"

    return [cur_GO, cur_label]


def query_helper(args):
    return query(*args)

def main():

    global pred_res_df
    global label_df

    process_options()

    pred_res_df = pandas.read_csv(args.input, engine='python', sep='\t', skip_footer=1, skiprows=3, names=['ID','GO','score'])
    label_df = pandas.read_csv(args.testing_label_file, sep='\t', names=['ID', 'GO'])
    with open(args.target_list, 'r') as f:
        target_list = f.read().splitlines()

    pred_res_df = pred_res_df[pred_res_df['ID'].isin(target_list)].reset_index(drop=True)
    label_df = label_df[label_df['ID'].isin(target_list)].reset_index(drop=True)
    pred_res_df['label'] = None

    query_args = []
    for i in range(0,len(pred_res_df.index)):
        query_args.append([i])

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
    GO_df = pandas.DataFrame(columns=["GO","label"])
    for i in range(0,len(results)):
        GO_df.loc[i] = results[i]

    GO_list = list(GO_df['GO'].unique())
    sta_df = pandas.DataFrame({'GO':GO_list, 'TP':[0]*len(GO_list), 'FP':[0]*len(GO_list), 'ratio':[0.0]*len(GO_list)})

    TP_df = GO_df[GO_df['label'] == 'TP'].groupby(['GO']).count().reset_index()
    FP_df = GO_df[GO_df['label'] == 'FP'].groupby(['GO']).count().reset_index()

    for i in range(0,len(TP_df.index)):
        cur_GO = TP_df.loc[i,'GO']
        sta_df.loc[GO_list.index(cur_GO), 'TP'] = TP_df.loc[i,'label']

    for i in range(0,len(FP_df.index)):
        cur_GO = FP_df.loc[i,'GO']
        sta_df.loc[GO_list.index(cur_GO), 'FP'] = FP_df.loc[i,'label']

    for i in range(0,len(sta_df.index)):
        if sta_df.loc[i,'TP'] != 0:
            sta_df.loc[i,'ratio'] = float(sta_df.loc[i,'FP'])/float(sta_df.loc[i,'TP'])
        else:
            sta_df.loc[i,'ratio'] = float('Inf')

    sta_df.to_csv(args.output,sep='\t',index=False, columns=['GO','ratio'])

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
