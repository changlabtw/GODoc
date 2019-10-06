import os
import sys
import pandas

global input_file
global output_file
global nlist_file

def process_options(argv = sys.argv):
    global input_file, output_file, nlist_file

    if len(argv) < 3:
		print "Usage: %s input_file output_file nlist_file" % argv[0]
		sys.exit(1)
    elif len(argv) == 3:
        input_file = argv[1]
        output_file = argv[2]
        nlist_file = None
    elif len(argv) == 4:
        input_file = argv[1]
        output_file = argv[2]
        nlist_file = argv[3]

    if not os.path.exists(input_file):
        print "input_file not found."
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

    df = pandas.read_csv(input_file, sep='\t' ,header=0)
    df = df[-df['org_class'].isnull()] #drop no answer protein
    amount = len(df.index)
    unpred = len(df[df['pred_ID'].isnull()].index)
    df = df[-df['pred_ID'].isnull()]
    df['org_class'] = df['org_class'].apply(lambda x: x.split(','))
    df['pred_class'] = df['pred_class'].apply(lambda x: x.split(','))
    df['reacll'] = df.apply(lambda x: float(len(intersection(x['org_class'],x['pred_class'])))/float(len(x['org_class'])), axis=1)
    df['precision'] = df.apply(lambda x: float(len(intersection(x['org_class'],x['pred_class'])))/float(len(x['pred_class'])), axis=1)
    df['f-measure'] = df.apply(fmeasure , axis=1)

    if nlist_file != None:
        with open(nlist_file, 'r') as f:
            nlist_list = f.read().splitlines()
        nlist = []
        for line in nlist_list:
            tmplist = set()
            pairs = filter(bool, line.split('\t'))
            for pair in pairs:
                tmplist.add(pair.split(',')[0])
            nlist.append(list(tmplist))
        for ind, fold in enumerate(nlist):
            r = df[df['ID'].isin(fold)]['reacll'].sum()/len(fold)
            p = df[df['ID'].isin(fold)]['precision'].sum()/len(fold)
            print "fold-" + str(ind)
            print "recall:\t" + str(r)
            print "precision:\t" + str(p)
            print "f-measure:\t" + str((2*r*p)/(r+p))

    print "overall"
    r = df['reacll'].sum()/len(df.index)
    p = df['precision'].sum()/len(df.index)
    print "recall:\t" + str(r)
    print "precision:\t" + str(p)
    print "f-measure:\t" + str((2*r*p)/(r+p))
    print "coverage:\t" + str(round(float(1) - float(unpred)/float(amount), 3))

main()
