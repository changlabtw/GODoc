# For clean CAFA2 training dataset SWISS to csv file
import os
import sys
import pandas
import time
import multiprocessing

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

def clean(ind):

    current = []
    current_NCBI = str(function_df.loc[ind,'NCBI'])
    current_ID = function_df.loc[ind,'Accession'].split(";")[0]
    current_goas = function_df.loc[ind,'GOAs'].split(";")
    for i, current_goa in enumerate(current_goas):
        current_go = current_goa.split(",")[0]
        current_namesapse = current_goa.split(",")[1]
        current_code = current_goa.split(",")[2]
        current.append([current_ID,current_NCBI,current_go, current_namesapse, current_code])

    return current

def clean_helper(args):
    return clean(*args)

def main():

    global function_df
    global res_df

    process_options()

    SwissFormat = ["ID", "NCBI", "Accession", "GOAs"]
    function_df = pandas.read_csv(function_file, sep="\t", names=SwissFormat, engine="python")

    res_df = pandas.DataFrame(columns=['ID','NCBI','GO','namespace','code'])

    pool = multiprocessing.Pool()
    clean_args = []

    for i in range(0,len(function_df.index)):
        clean_args.append([i])

    p = multiprocessing.Pool()
    rs = p.map_async(clean_helper, clean_args)
    p.close() # No more work
    while (True):
      if (rs.ready()): break
      remaining = rs._number_left
      print "Waiting for", remaining, "tasks to complete..."
      time.sleep(2)

    results = rs.get()
    for result in results:
        for row in result:
            res_df.loc[len(res_df.index)] = row

    res_df['source'] = "SWISS"
    res_df['note'] = "org"
    res_df.to_csv(output_file, sep=",", index=False)

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
