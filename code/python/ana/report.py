import os
import sys
import pandas

global input_file

def process_options(argv = sys.argv):
    global input_file

    if len(argv) < 2:
		print "Usage: %s input_file" % argv[0]
		sys.exit(1)

    input_file = argv[1]

    if not os.path.exists(input_file):
        print "input_file not found."
        sys.exit(1)

def main():

    process_options()

    df = pandas.read_csv(input_file, sep='\t' ,names=['ID','label'])

    sta_id = df.groupby(['ID']).count()
    sta_id = sta_id.sort_values(['label'],ascending=False)

    sta_label = df.groupby(['label']).count()
    sta_label = sta_label.sort_values(['ID'],ascending=False)

    print "There are " + str(len(df.index)) + " unique pair."
    print "There are " + str(len(sta_id.index)) + " proteins."
    print "There are " + str(len(sta_label.index)) + " labels."
    print "\nGroup by ID:"
    print sta_id.describe()
    print "\nGroup by label:"
    print sta_label.describe()

main()
