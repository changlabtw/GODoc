import os
import sys
import pandas
import random

global input_file
global output_file
global num_fold


def process_options(argv = sys.argv):
    global input_file, output_file, num_fold

    if len(argv) < 4:
		print "Usage: %s input_file output_file num_fold" % argv[0]
		sys.exit(1)

    input_file = argv[1]
    output_file = argv[2]
    num_fold = int(argv[3])

    if not os.path.exists(input_file):
        print "input_file not found."
        sys.exit(1)

def main():

    process_options()

    df = pandas.read_csv(input_file, sep='\t' ,names=['ID','GO'])
    sta = df.groupby(['ID']).count()
    sta = sta.sort_values(['GO'],ascending=False)
    folds = []

    for foldInd in range(0,num_fold):
        folds.append([])

    index_list = sta.index
    random.shuffle(index_list)
    for ind in range(0,len(index_list)):
        folds[ind%num_fold].append(index_list[ind])
    with open(output_file, 'w') as f:
        for foldInd in range(0,num_fold):
            currentdf = df.loc[df['ID'].isin(folds[foldInd])]
            out_str = ""
            for i in range(0,len(currentdf.index)):
                out_str += currentdf.iloc[i,0] + "," + currentdf.iloc[i,1] + "\t"
            f.write(out_str + '\n')

main()
