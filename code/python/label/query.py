import os
import sys
import pandas
import time
import sqlite3
import argparse

global args

def process_options():
    global args

    parser = argparse.ArgumentParser(description='Query label DB')
    parser.add_argument('-db','--database',help='sqlite3 DB')
    parser.add_argument('-s','--slt',help='SQL SELECT', default='ID,GO')
    parser.add_argument('-f','--frm',help='SQL FROM', default='label')
    parser.add_argument('-w','--whr',help='SQL WHERE', default='source="SWISS" and namespace="C"')
    parser.add_argument('-o','--output',help='output file name', default='label.tsv')

    args = parser.parse_args()

    if not os.path.exists(args.database):
        print "sqlite3 DB not found."

def main():

    process_options()

    sqlDB = args.database

    conn = sqlite3.connect(sqlDB)

    cursor = conn.execute("SELECT %s FROM %s WHERE %s" % (args.slt, args.frm, args.whr))

    data = [[],[]]
    for row in cursor:
        data[0].append(row[0])
        data[1].append(row[1])

    res_df = pandas.DataFrame({'ID':data[0],'GO':data[1]})
    res_df = res_df.drop_duplicates(['ID','GO'])
    res_df = res_df[['ID','GO']]
    res_df.to_csv(args.output, sep="\t", index=False, header=False)

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
