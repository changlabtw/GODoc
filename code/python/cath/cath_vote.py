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

def process_options(argv = sys.argv):
    global args

    parser = argparse.ArgumentParser(description='Vote by knn file with cath filter.')
    parser.add_argument('-i', '--knn_file', help='KNN file')
    parser.add_argument('-l', '--label_file', help='Training label file')
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

def vote(ind, score_formula):

    global knn_df
    global label_df

    dist_pairs = knn_df.loc[ind,'pred_ID'].split(";")
    dist_df = pandas.DataFrame(columns=["ID","dist"])
    for i, pair in enumerate(dist_pairs):
        dist_df.loc[i] = [pair.split(',')[0], float(pair.split(',')[1])]

    gos = pandas.DataFrame(columns=["GO","score"])

    for j in range(0,len(dist_df.index)):
        if dist_df.loc[j,"dist"] == 0.0:
            # skip if 1NN is itself
            continue
        current_gos = label_df[label_df["ID"] == dist_df.loc[j,"ID"]]["GO"].values

        if score_formula == 0:
            # score = 1/dist
            current_score = [1.0/dist_df.loc[j,"dist"]]
            new_rows = pandas.DataFrame({"GO":current_gos, "score": current_score*len(current_gos)})
        elif score_formula == 1:
            # score = log(1/dist)
            current_score = [numpy.log(1.0/dist_df.loc[j,"dist"])]
            new_rows = pandas.DataFrame({"GO":current_gos, "score": current_score*len(current_gos)})
        elif score_formula == 2:
            # score = sqrt(1/dist)
            current_score = [numpy.sqrt(1.0/dist_df.loc[j,"dist"])]
            new_rows = pandas.DataFrame({"GO":current_gos, "score": current_score*len(current_gos)})
        elif score_formula == 3:
            # score = sqrt(1/dist)
            current_score = [1.0]
            new_rows = pandas.DataFrame({"GO":current_gos, "score": current_score*len(current_gos)})
        gos = gos.append(new_rows)

    gos_sta = gos.groupby("GO").sum().sort_values(by=["score"], ascending=False).reset_index()

    if score_formula == 3:
        gos_sta['map_score'] = 1.0
    else:
        gos_sta['map_score'] = gos_sta['score']/gos_sta['score'].max()
    ID = knn_df.loc[ind,'ID']

    score_list = []
    for k in range(0,len(gos_sta.index)):
        score_list.append( ID + '\t' + gos_sta.loc[k,'GO'] + '\t' + format(round(gos_sta.loc[k,'map_score'],2),'.2f') + '\n' )

    return score_list

def vote_helper(args):
    return vote(*args)

def main():

    global knn_df
    global label_df

    process_options()

    threshold = 0.5
    knn_df = pandas.read_csv(args.knn_file, sep='\t' ,header=0)
    label_df = pandas.read_csv(args.label_file, sep='\t' ,names=["ID","GO"])

    print "Unpred protein amount: %i" % len(knn_df[knn_df['pred_ID'].isnull()].index)
    knn_df = knn_df[-knn_df['pred_ID'].isnull()].reset_index(drop=True) #drop unpred protein

    knn_df['count_list'] = knn_df['pred_ID'].apply(lambda x: [int(pair.split(',')[2]) for pair in x.split(';')] )
    knn_df['dist_list'] = knn_df['pred_ID'].apply(lambda x: [float(pair.split(',')[1]) for pair in x.split(';')] )
    knn_df['count_max'] = knn_df['count_list'].apply(lambda x: max(x) )
    knn_df['dist_min'] = knn_df['dist_list'].apply(lambda x: min(x) )

    knn_df['pred_GO'] =None
    knn_df['GO_sta'] = None
    for i in range(0,len(knn_df)):
        if knn_df.loc[i,'count_max'] > 1:
            cur_pred_IDs = [ pair.split(',')[0] for pair in knn_df.loc[i,'pred_ID'].split(';') ]
        else:
            cur_pred_IDs = [(knn_df.loc[i,'pred_ID'].split(';')[knn_df.loc[i,'dist_list'].index(knn_df.loc[i,'dist_min'])]).split(',')[0]]
        pred_GOs = label_df[label_df['ID'].isin(cur_pred_IDs)]['GO'].values
        cur_sta = pandas.Series(pred_GOs).value_counts()
        knn_df.at[i,'GO_sta'] = cur_sta
        knn_df.at[i,'pred_GO'] = list(cur_sta[cur_sta/(cur_sta.max())>threshold].index)

    # knn_df['GO_sta'] = None
    # for i in range(0,len(knn_df)):
    #     knn_df.at[i.'GO_sta'] = knn_df.loc[i,'pred_ID']
    #
    #
    # pool = multiprocessing.Pool()
    # vote_args = []
    #
    # for i in range(0,len(knn_df.index)):
    # # for i in range(1,2):
    #     vote_args.append([i, args.score_formula])
    #
    # p = multiprocessing.Pool()
    # rs = p.map_async(vote_helper, vote_args)
    # p.close() # No more work
    # while (True):
    #   if (rs.ready()): break
    #   remaining = rs._number_left
    #   print "Waiting for", remaining, "tasks to complete..."
    #   time.sleep(2)

    with open(args.output_file, 'w') as f:
        f.write("AUTHOR TEAM_NAME\n")
        f.write("MODEL 1\n")
        f.write("KEYWORDS\tCATH Vote\n")
        for i in range(0,len(knn_df)):
            cur_ID = knn_df.loc[i,'ID']
            for GO in knn_df.loc[i,'pred_GO']:
                f.write(cur_ID)
                f.write('\t')
                f.write(GO)
                f.write('\t')
                f.write('1.00')
                f.write('\n')
        f.write("END\n")

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
