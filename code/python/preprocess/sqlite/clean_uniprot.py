# For clean CAFA2 training dataset UniProt to csv file
import os
import sys
import pandas
import time

global function_file
global output_file
global function_df

def process_options(argv = sys.argv):
    global function_file
    global output_file

    if len(argv) < 3:
		print "Usage: %s function_file output_file" % argv[0]
		sys.exit(1)

    function_file = argv[1]
    output_file = argv[2]

    if not os.path.exists(function_file):
        print "function_file not found."
        sys.exit(1)

def main():

    global function_df

    process_options()

    UniProtFormat = ["ID", "NCBI", "Qualifier", "GO", "namespace", "code"]
    function_df = pandas.read_csv(function_file, sep="\t|,", names=UniProtFormat, engine="python")

    function_df['source'] = "UniProt"
    function_df['note'] = "org"
    function_df.drop('Qualifier',axis=1,inplace=True)

    function_df.to_csv(output_file, sep=",", index=False)

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
