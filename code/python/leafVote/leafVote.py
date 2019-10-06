import os
import sys
import pandas
import numpy
import time
import multiprocessing
import argparse

global args
global knn_df
global label_df
global normalize_max

def process_options(argv = sys.argv):
    global args

    parser = argparse.ArgumentParser(description='KNN for tsv or csv vector files.')
    parser.add_argument('-i', '--knn_file', help='KNN output with distance file')
    parser.add_argument('-b','--big', action='store_true', help='Switch to support large KNN file')
    parser.add_argument('-single','--single', action='store_true', help='Enable single processing')
    parser.add_argument('-k','--k',help='KNN number', type=int, default=0)
    parser.add_argument('-l', '--label_file', help='Training label file')
    parser.add_argument('-s','--score_formula', help='Score formula, 0: 1/dist, 1: log(1/dist), 2: sqrt(1/dist), 3: 1.0, 4: (1/dist)/normalize_max, 5: student_C, 6: count', type=int, choices=[0,1,2,3,4,5,6], default=0)
    parser.add_argument('-o','--output_file',help='Output file name', default='vote_score.txt')

    args = parser.parse_args()

    if not os.path.exists(args.knn_file):
        print "knn_file not found."
        sys.exit(1)

    if not os.path.exists(args.label_file):
        print "label_file not found."
        sys.exit(1)

    if os.path.exists(args.output_file):
        print "output_file already exits."
        sys.exit(1)

def fun_search(ID):
    global label_df
    return pandas.Series(label_df[label_df['ID'].searchsorted(ID, 'left')[0]:label_df['ID'].searchsorted(ID, 'right')[0]]['GO']).values

def vote(ind, score_formula):

    global knn_df
    global label_df

    if args.big:
        ID = knn_df[ind][0]
        dist_pairs = knn_df[ind][1].split(";")
    else:
        ID = knn_df.values[ind,0]
        dist_pairs = knn_df.values[ind,1].split(";")

    dist_df = pandas.DataFrame([ [pair.split(',')[0], float(pair.split(',')[1])] for pair in dist_pairs], columns=["ID","dist"])

    if args.k != 0:
        dist_df = dist_df.sort_values(['dist']).reset_index(drop=True)[0:args.k]

    gos = []

    for j in range(0,len(dist_df.index)):
        cur_dist = dist_df.values[j,1]
        if cur_dist == 0.0:
            # skip if 1NN is itself
            continue
        try:
            current_gos = fun_search(dist_df.values[j,0])
        except KeyError:
            continue

        if score_formula == 0 or score_formula == 4 or score_formula==5:
            # score = 1/dist
            current_score = [1.0/cur_dist]
        elif score_formula == 1:
            # score = log(1/dist)
            current_score = [numpy.log(1.0/cur_dist)]
        elif score_formula == 2:
            # score = sqrt(1/dist)
            current_score = [numpy.sqrt(1.0/cur_dist)]
        elif score_formula == 3 or score_formula == 6:
            # score = sqrt(1/dist)
            current_score = [1.0]
        new_rows = zip(current_gos, current_score*len(current_gos))
        gos = gos + new_rows

    if len(gos)==0:
        return []

    gos = pandas.DataFrame(gos, columns=["GO","score"])
    gos_sta = gos.groupby("GO").sum().sort_values(by=["score"], ascending=False).reset_index()

    if score_formula == 3:
        gos_sta['map_score'] = 1.0
    elif score_formula == 4:
        gos_sta['map_score'] = gos_sta['score'].apply(lambda x: x/(1.0/normalize_max) if x < 1.0/normalize_max else 1.00 )
    elif score_formula == 5:
        try:
            gos_count = gos.groupby("GO").count()
            max_count = gos_count.max()
            gos_sta['score'] = gos_sta.apply(lambda x: x['score']*gos_count.loc[x['GO']]/max_count, axis=1)
            gos_sta['map_score'] = gos_sta['score']/gos_sta['score'].max()
        except ValueError:
            print gos_sta
            gos_sta['map_score'] = gos_sta['score']/gos_sta['score'].max()
    else:
        max_score = gos_sta['score'].max()
        gos_sta['map_score'] = gos_sta['score']/max_score

    score_list = gos_sta.apply(lambda x: ID + '\t' + x['GO'] + '\t' + format(round(x['map_score'],2),'.2f') + '\n',axis=1)

    return score_list

def vote_helper(args):
    return vote(*args)

def main():

    global knn_df
    global label_df
    global normalize_max
    method = ['1/dist','log(1/dist)','sqrt(1/dist)','None','(1/dist)/normalize_max','student_C','count']

    process_options()

    if args.big:
        knn_df = []
        count = 0
        with open(args.knn_file, 'r') as f:
            lines = f.read().splitlines()
            for line in lines[1:]:
                cur_row = line.split('\t')
                if len(cur_row) != 2:
                    count = count + 1
                else:
                    knn_df.append([cur_row[0],cur_row[1]])
            print "Unpred protein amount: %i" % count
    else:
        knn_df = pandas.read_csv(args.knn_file, sep='\t' ,header=0)
        print "Unpred protein amount: %i" % len(knn_df[knn_df['pred_ID'].isnull()].index)
        knn_df = knn_df[-knn_df['pred_ID'].isnull()].reset_index(drop=True) #drop unpred protein

    label_df = pandas.read_csv(args.label_file, sep='\t' ,names=["ID","GO"])
    label_df = label_df.sort_values("ID")

    if args.score_formula == 4:
        dist_list = []
        for i in range(0,len(knn_df)):
            dist_list = dist_list + [ float(pair.split(',')[1]) for pair in knn_df.loc[i,'pred_ID'].split(';') if float(pair.split(',')[1]) != 0 ]
        normalize_max = numpy.min(dist_list)

    if args.single:
        results = []
        for i in range(0,len(knn_df.index)):
            results.append(vote(i, args.score_formula))
        with open(args.output_file, 'w') as f:
            f.write("AUTHOR TEAM_NAME\n")
            f.write("MODEL 1\n")
            f.write("KEYWORDS\t"+method[args.score_formula]+"\n")
            for str_list in results:
                for line in str_list:
                    f.write(line)
            f.write("END\n")
    else:
        pool = multiprocessing.Pool()
        vote_args = []

        if args.big:
            for i in range(0,len(knn_df)):
                vote_args.append([i, args.score_formula])
        else:
            for i in range(0,len(knn_df.index)):
                vote_args.append([i, args.score_formula])

        p = multiprocessing.Pool()
        rs = p.map_async(vote_helper, vote_args)
        p.close() # No more work
        while (True):
          if (rs.ready()): break
          remaining = rs._number_left
          print "Waiting for", remaining, "tasks to complete..."
          time.sleep(2)

        with open(args.output_file, 'w') as f:
            f.write("AUTHOR TEAM_NAME\n")
            f.write("MODEL 1\n")
            f.write("KEYWORDS\t"+method[args.score_formula]+"\n")
            results = rs.get()
            for str_list in results:
                for line in str_list:
                    f.write(line)
            f.write("END\n")

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
