import os
import sys
import pandas

global pred_res_file
global train_label_file
global test_label_file

def process_options(argv = sys.argv):
    global pred_res_file
    global train_label_file
    global test_label_file

    if len(argv) < 4:
		print "Usage: %s pred_res_file train_label_file test_label_file" % argv[0]
		sys.exit(1)
    elif len(argv) == 4:
        pred_res_file = argv[1]
        train_label_file = argv[2]
        test_label_file = argv[3]

    if not os.path.exists(pred_res_file):
        print "pred_res_file not found."
        sys.exit(1)

    if not os.path.exists(train_label_file):
        print "train_label_file not found."
        sys.exit(1)

    if not os.path.exists(test_label_file):
        print "test_label_file not found."
        sys.exit(1)

def intersection(x,y):
    return (set(x) & set(y))

def fmeasure(x):
    if x['reacll']+x['precision'] == 0:
        return 0
    else:
        return (2*x['reacll']*x['precision'])/(x['reacll']+x['precision'])

def main():

    process_options()

    df = pandas.read_csv(pred_res_file, sep="\t", names=["ID","pred_ID"])
    train_label_df = pandas.read_csv(train_label_file, sep="\t", names=["ID","GO"])
    test_label_df = pandas.read_csv(test_label_file, sep="\t", names=["ID","GO"])

    for i in range(0,len(df.index)):

        df.loc[i,'org_class'] = ','.join(test_label_df[ test_label_df['ID'] == df.loc[i,'ID'] ]['GO'].values)
        df.loc[i,'pred_class'] = ','.join(train_label_df[ train_label_df['ID'] == df.loc[i,'pred_ID'] ]['GO'].values)

    df = df[-df['org_class'].isnull()] #drop no answer protein
    amount = len(df.index)
    unpred = len(df[df['pred_ID'].isnull()].index)
    df = df[-(df['org_class'] == "")]
    df['org_class'] = df['org_class'].apply(lambda x: x.split(','))
    df['pred_class'] = df['pred_class'].apply(lambda x: x.split(','))
    df['reacll'] = df.apply(lambda x: float(len(intersection(x['org_class'],x['pred_class'])))/float(len(x['org_class'])), axis=1)
    df['precision'] = df.apply(lambda x: float(len(intersection(x['org_class'],x['pred_class'])))/float(len(x['pred_class'])), axis=1)
    df['f-measure'] = df.apply(fmeasure , axis=1)

    print "overall"
    r = df['reacll'].sum()/len(df.index)
    p = df['precision'].sum()/len(df.index)
    print "recall:\t" + str(r)
    print "precision:\t" + str(p)
    print "f-measure:\t" + str((2*r*p)/(r+p))
    print "coverage:\t" + str(round(float(1) - float(unpred)/float(amount), 3))

main()
