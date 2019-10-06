import os
import sys
import pandas

global input_file
global output_file
global new_ID_file

def process_options(argv = sys.argv):
    global input_file, output_file, new_ID_file

    if len(argv) < 4:
		print "Usage: %s input_file new_ID_file output_file" % argv[0]
		sys.exit(1)

    input_file = argv[1]
    new_ID_file = argv[2]
    output_file = argv[3]

    if not os.path.exists(input_file):
        print "input_file not found."
        sys.exit(1)

    if not os.path.exists(new_ID_file):
        print "new_ID_file not found."
        sys.exit(1)

def main():

    process_options()

    df = pandas.read_csv(input_file, sep='\t' ,header=None)

    newID = pandas.read_csv(new_ID_file, sep='\t', header=None)

    for i in range(0,len(df.index)):
        new = newID[1][newID[0] == df[0][i]].values
        if len(new) == 1:
            df[0][i] = new[0]
        else:
            print "no pair."
            sys.exit(1)

    df.to_csv(output_file, sep="\t", index=False ,header=False)

main()
