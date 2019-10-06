import os
import sys
import pandas
import time
import json
import urllib2
import argparse
import multiprocessing

global args

def process_options():
    global args

    parser = argparse.ArgumentParser(description='Get superfamily and GO mapping table from cath.')
    parser.add_argument('-i', '--input', help='superfamily list')
    parser.add_argument('-o','--output',help='Output file name', default='superfamily_go.tsv')

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print "superfamily list not found."
        sys.exit(1)

    if os.path.exists(args.output):
        print "output allready exists."
        sys.exit(1)

def query(sf):

    root = {'Biological Process':'GO:0008150','Cellular Component':'GO:0003674','Molecular Function':'GO:0005575'}
    # color = {'#4572A7':'P','#AA4643':'C','#89A54E':'F'}
    color = {}

    cur_res = []
    cath_url = 'http://www.cathdb.info/version/v4_1_0/superfamily/'
    cur_url = cath_url + sf + '/highcharts/go'
    webCur_url = urllib2.urlopen(cur_url)
    if (webCur_url.getcode() == 200):
        data = json.loads(webCur_url.read())
        if (len(data['series']) != 1):
            for go in data['series'][0]['data']:
                if go['color'] == '#CCCCCC':
                    continue
                else:
                    if go['name'] == 'Biological Process':
                        color[go['color']] = 'P'
                    elif go['name'] == 'Cellular Component':
                        color[go['color']] = 'C'
                    elif go['name'] == 'Molecular Function':
                        color[go['color']] = 'F'
                    cur_res.append([sf,root[go['name']],color[go['color']],go['y']])
            for go in data['series'][1]['data']:
                if go['color'] == '#CCCCCC':
                    continue
                else:
                    cur_res.append([sf,str(go['name']).split(': ')[0],color[go['color']],go['y']])
        else:
            print 'skip' + sf
    else:
        print 'error'

    return cur_res

def query_helper(args):
    return query(*args)

def main():

    process_options()

    sf_df = pandas.read_csv(args.input, sep='\t', comment='#', names=['ID','s','e','name'])
    sf_list = sf_df['ID'].unique()

    query_args = []
    for sf in sf_list:
        query_args.append([sf])

    pool = multiprocessing.Pool()
    p = multiprocessing.Pool()
    rs = p.map_async(query_helper, query_args)
    p.close() # No more work
    while (True):
      if (rs.ready()): break
      remaining = rs._number_left
      print "Waiting for", remaining, "tasks to complete..."
      time.sleep(2)

    results = rs.get()
    with open(args.output, 'w') as f:
        for rows in results:
            for row in rows:
                f.write(row[0])
                f.write('\t')
                f.write(row[1])
                f.write('\t')
                f.write(row[2])
                f.write('\t')
                f.write(str(row[3]))
                f.write('\n')

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
