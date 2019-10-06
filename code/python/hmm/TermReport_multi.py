import os
import sys
import pandas
import time
import argparse
import multiprocessing
from goatools.obo_parser import GODag, GraphEngines

global args
global res_df
global label_df
global model_list
global godb

#python ../TermReport_multi.py -i hmm_scan_result.txt -l new_propagated_MFO.txt -m mfo_model_list.txt -t mfo_all_typex.txt -db ../../propagate/go-basic.obo
#python ../TermReport_multi.py -i hmm_scan_result.txt -l new_propagated_CCO.txt -m cco_model_list.txt -t cco_all_typex.txt -db ../../propagate/go-basic.obo
#python ../TermReport_multi.py -i hmm_scan_result.txt -l new_propagated_BPO.txt -m bpo_model_list.txt -t bpo_all_typex.txt -db ../../propagate/go-basic.obo

def process_options():
    global args

    parser = argparse.ArgumentParser(description='HMM Model Term Centric Analysis')
    parser.add_argument('-i', '--input_file', help='hmmscan results file')
    parser.add_argument('-l', '--label_file', help='ground truth label file')
    parser.add_argument('-m', '--model_list', help='GO with HMM model list')
    parser.add_argument('-t', '--target_list', help='target protein ID list')
    parser.add_argument('-a', '--all', action='store_true', help='without using target_list')
    parser.add_argument('-db', '--go_db', help='gene ontology database')
    parser.add_argument('-o', '--output_file', default='report.csv', help='analysis csv file')

    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print "input_file not found."
        sys.exit(1)

    if not os.path.exists(args.label_file):
        print "label_file not found."
        sys.exit(1)

    if not os.path.exists(args.model_list):
        print "model_list not found."
        sys.exit(1)

    if not os.path.exists(args.target_list) and not args.all:
        print "target_list not found."
        sys.exit(1)

    if not os.path.exists(args.go_db):
        print "go_db not found."
        sys.exit(1)

    if os.path.exists(args.output_file):
        print "output_file already exists."
        sys.exit(1)

def reportGO(cur_go):
    report_col = ['GO','TP','FN','FP','precision','recall','fmeasure','depth','model_amount',
                  'TP_std','TP_min','TP_25%','TP_50%','TP_75%','TP_max',
                  'FP_std','FP_min','FP_25%','FP_50%','FP_75%','FP_max']

    cur_row = pandas.DataFrame(None, columns=report_col)
    cur_row.loc[0,['GO']] = cur_go

    #TP, FP and distribution
    curTP_df = res_df[(res_df['target'] == cur_go) & (res_df['label'] == 'TP')]
    curFP_df = res_df[(res_df['target'] == cur_go) & (res_df['label'] == 'FP')]
    TP_amount = len(curTP_df.index)
    cur_row.loc[0,['TP']] = TP_amount
    FP_amount = len(curFP_df.index)
    cur_row.loc[0,['FP']] = FP_amount
    if TP_amount != 0 or FP_amount !=0:
        distri_df = res_df[res_df['target'] == cur_go].loc[:,['b_E-value','label']]
        if TP_amount != 0:
            TP_distri = distri_df[distri_df['label']=='TP']['b_E-value'].describe()
            cur_row.loc[0,['TP_std','TP_min','TP_25%','TP_50%','TP_75%','TP_max']] = [TP_distri['std'],TP_distri['min'],TP_distri['25%'],TP_distri['50%'],TP_distri['75%'],TP_distri['max']]
        if FP_amount != 0:
            FP_distri = distri_df[distri_df['label']=='FP']['b_E-value'].describe()
            cur_row.loc[0,['FP_std','FP_min','FP_25%','FP_50%','FP_75%','FP_max']] = [FP_distri['std'],FP_distri['min'],FP_distri['25%'],FP_distri['50%'],FP_distri['75%'],FP_distri['max']]

    #FN
    FN_amount = len(label_df[label_df['GO'] == cur_go].index)
    cur_row.loc[0,['FN']] = FN_amount

    #precision, recall, fmeasure
    cur_pr = ( 0 if (FP_amount + TP_amount)==0 else TP_amount / float(FP_amount + TP_amount))
    cur_rc = ( 0 if (FN_amount + TP_amount)==0 else TP_amount / float(FN_amount + TP_amount))
    cur_f = ( 0 if (cur_pr + cur_rc)==0 else 2*cur_pr*cur_rc / (cur_pr + cur_rc))
    cur_row.loc[0,['precision','recall','fmeasure']] = [cur_pr, cur_rc, cur_f]

    #model_count
    cur_row.loc[0,['model_amount']] = model_list.count(cur_go)

    #depth at ontology
    cur_row.loc[0,['depth']] = godb.query_term(cur_go).depth

    return cur_row.loc[0].values

def reportGO_helper(args):
    return reportGO(*args)

def main():

    global res_df
    global label_df
    global model_list
    global godb

    process_options()

    godb = GODag(args.go_db)

    #target: GO, query: protein ID
    col = ['target', 'target_accession', 'query', 'query_accession', 'f_E-value', 'f_score', 'f_bias',
           'b_E-value', 'b_score', 'b_bias', 'exp', 'reg', 'clu', 'ov', 'env', 'dom', 'rep', 'inc',
           ' description']

    res_df = pandas.read_csv(args.input_file, delim_whitespace=True, comment='#', names=col, engine='python')
    res_df = res_df.drop_duplicates(['query', 'target']).reset_index(drop=True)
    res_df['label'] = None

    label_df = pandas.read_csv(args.label_file, names=['ID','GO'], sep='\t')

    model_list = []
    with open(args.model_list, 'r') as f:
        lines = f.read().splitlines()
        for line in lines:
            model_list.append(line.split('_')[0])

    #prepare report dataframe
    report_col = ['GO','TP','FN','FP','precision','recall','fmeasure','depth','model_amount',
                  'TP_std','TP_min','TP_25%','TP_50%','TP_75%','TP_max',
                  'FP_std','FP_min','FP_25%','FP_50%','FP_75%','FP_max']

    report_df = pandas.DataFrame(None, columns=report_col)
    report_df['GO'] = list(set(model_list))

    #filter target at res_df and label_df
    if not(args.all):
        target_list = []
        with open(args.target_list, 'r') as f:
            target_list = f.read().splitlines()
        res_df = res_df[res_df['query'].isin(target_list)].reset_index(drop=True)
        label_df = label_df[label_df['ID'].isin(target_list)].reset_index(drop=True)


    #label TP,FP in hmmscan_result
    for i in range(0,len(res_df.index)):
        pred_pair = res_df.loc[i,['target','query']].values
        if len(label_df[(label_df['GO'] == pred_pair[0]) & (label_df['ID'] == pred_pair[1])]) !=0 :
            res_df.loc[i,['label']] = 'TP'
            label_df = label_df[(label_df['GO'] != pred_pair[0]) | (label_df['ID'] != pred_pair[1])] #drop TP in label_df
        else:
            res_df.loc[i,['label']] = 'FP'

    reportGO_args = []
    for i in range(0,len(report_df.index)):
        reportGO_args.append([report_df.loc[i,'GO']])

    pool = multiprocessing.Pool()
    p = multiprocessing.Pool()
    rs = p.map_async(reportGO_helper, reportGO_args)
    p.close() # No more work
    while (True):
      if (rs.ready()): break
      remaining = rs._number_left
      print "Waiting for", remaining, "tasks to complete..."
      time.sleep(2)

    results = rs.get()
    for i in range(0,len(results)):
        report_df.loc[i] = results[i]

    report_df.to_csv(args.output_file, index=False)


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
