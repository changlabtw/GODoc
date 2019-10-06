import os
import sys
import pandas

global input_file
global output_file
global new_label_file

def process_options(argv = sys.argv):
    global input_file, output_file, new_label_file

    if len(argv) < 4:
		print "Usage: %s input_file new_label_file output_file" % argv[0]
		sys.exit(1)

    input_file = argv[1]
    new_label_file = argv[2]
    output_file = argv[3]

    if not os.path.exists(input_file):
        print "input_file not found."
        sys.exit(1)

    if not os.path.exists(new_label_file):
        print "new_label_file not found."
        sys.exit(1)

def main():

    process_options()

    df = pandas.read_csv(input_file, sep='\t' ,header=0)

    label = pandas.read_csv(new_label_file, sep='\t', header=None)

    for i in range(0,len(df.index)):
        new_labels = label[label[0] == df['ID'][i]][1].values
        if len(new_labels)==0:
            df['org_class'][i] = "NA"
        else:
            df['org_class'][i] = ','.join(label[label[0] == df['ID'][i]][1].values)

    df.to_csv(output_file, sep="\t")

main()
