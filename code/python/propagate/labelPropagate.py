import os
import sys
import pandas
import time
import multiprocessing
from goatools.obo_parser import GODag, GraphEngines
import argparse

global args
global label_df
global godb

def process_options():
    global args

    parser = argparse.ArgumentParser(description='Get predict GO\'s parents of GO term.')
    parser.add_argument('-i', '--label_file', help='function label file', required=True)
    parser.add_argument('-o', '--output_file', help='function label file in propagated', default='propagated_function.tsv')
    parser.add_argument('-db','--database', help='Gene Ontology Database', default='go-basic.obo')

    args = parser.parse_args()

    if not os.path.exists(args.label_file):
        print "label_file not found."
        sys.exit(1)

    if not os.path.exists(args.database):
        print "database not found."
        sys.exit(1)

def findParents(ID):


    current_df = label_df[label_df['ID']==ID].reset_index(drop=True)
    propagated_df = pandas.DataFrame(columns=['ID','GO'])

    for i in range(0,len(current_df.index)):
        current_leaf = current_df.loc[i,'GO']
        try:
            current_parents = list(godb.query_term(current_leaf).get_all_parents())
        except AttributeError:
            print "skip " + current_leaf + ", because of error GO."
            continue
        current_list = [current_leaf] + current_parents
        new_rows = pandas.DataFrame({'ID':[ID] * len(current_list), 'GO':current_list })
        propagated_df = propagated_df.append(new_rows)

    propagated_df = propagated_df.drop_duplicates().reset_index(drop=True)

    return [propagated_df['ID'].values, propagated_df['GO'].values]

def findParents_helper(args):
    return findParents(*args)

def main():

    global label_df
    global godb

    process_options()

    label_df = pandas.read_csv(args.label_file, sep="\t", names=['ID','GO'])

    godb = GODag(args.database)

    findParents_args = []
    for ID in label_df['ID'].unique():
        findParents_args.append([ID])

    pool = multiprocessing.Pool()
    p = multiprocessing.Pool()
    rs = p.map_async(findParents_helper, findParents_args)
    p.close() # No more work
    while (True):
      if (rs.ready()): break
      remaining = rs._number_left
      print "Waiting for", remaining, "tasks to complete..."
      time.sleep(2)


    results = rs.get()
    with open(args.output_file, 'w') as f:
        for rows in results:
            for i in range(0,len(rows[0])):
                f.write(rows[0][i])
                f.write('\t')
                f.write(rows[1][i])
                f.write('\n')

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
