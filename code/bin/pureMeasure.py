#!/usr/bin/env python
import os
import sys
import pandas

global pred_res_file
global output_file
global pred_res_df

def process_options(argv = sys.argv):
    global pred_res_file
    global output_file

    if len(argv) < 3:
		print "Usage: %s pred_res_file output_file" % argv[0]
		sys.exit(1)
    elif len(argv) == 3:
        pred_res_file = argv[1]
        output_file = argv[2]

    if not os.path.exists(pred_res_file):
        print "pred_res_file not found."
        sys.exit(1)

def intersection(x,y):
    return (set(x) & set(y))

def fmeasure(x):
    if x['recall']+x['precision'] == 0:
        return 0
    else:
        return (2*x['recall']*x['precision'])/(x['recall']+x['precision'])

def main():

    global pred_res_df

    process_options()

    pred_res_df = pandas.read_csv(pred_res_file, sep="\t", header=0) # names = ['ID', 'pred_ID', 'org_class', 'pred_class']

    pred_res_df = pred_res_df[-pred_res_df['org_class'].isnull()].reset_index(drop=True) # drop no answer protein

    amount = len(pred_res_df.index) # get protein with answer amount for coverage
    unpred = len(pred_res_df[pred_res_df['pred_ID'].isnull()].index) # get unpred amount for coverage
    pred_res_df = pred_res_df[-pred_res_df['pred_ID'].isnull()].reset_index(drop=True) #drop unpred protein

    pred_res_df['org_class'] = pred_res_df['org_class'].apply(lambda x: x.split(','))
    pred_res_df['pred_class'] = pred_res_df['pred_class'].apply(lambda x: x.split(','))
    pred_res_df['recall'] = pred_res_df.apply(lambda x: float(len(intersection(x['org_class'],x['pred_class'])))/float(len(x['org_class'])), axis=1)
    pred_res_df['precision'] = pred_res_df.apply(lambda x: float(len(intersection(x['org_class'],x['pred_class'])))/float(len(x['pred_class'])), axis=1)
    pred_res_df['f-measure'] = pred_res_df.apply(fmeasure , axis=1)

    recall = pred_res_df['recall'].sum()/len(pred_res_df.index)
    precision = pred_res_df['precision'].sum()/len(pred_res_df.index)
    if recall + precision == 0:
        f1 = 0
    else:
        f1 = (2*recall*precision)/(recall+precision)

    with file(output_file, 'w') as f:
        f.write("recall\t%f\n" % recall)
        f.write("precision\t%f\n" % precision)
        f.write("f-measure\t%f\n" % f1)
        f.write("coverage\t%.3f\n" % (float(1) - float(unpred)/float(amount)))

main()
