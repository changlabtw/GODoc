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
global res_df

def process_options(argv = sys.argv):
    global args

    parser = argparse.ArgumentParser(description='KNN for tsv or csv vector files.')
    parser.add_argument('-i', '--knn_file', help='KNN output with distance file')
    parser.add_argument('-l', '--label_file', help='Training label file')
    parser.add_argument('-o','--output_folder',help='Output folder name', default='results')

    args = parser.parse_args()

    if not os.path.exists(args.knn_file):
        print "knn_file not found."
        sys.exit(1)

    if not os.path.exists(args.label_file):
        print "label_file not found."
        sys.exit(1)

    if not os.path.exists(args.output_folder):
        os.mkdir(args.output_folder)

    if os.listdir(args.output_folder) != []:
        print "output_folder isn't empty."
        sys.exit(1)

def vote(ind):

    global knn_df
    global label_df

    dist_pairs = knn_df.loc[ind,'pred_ID'].split(";")
    dist_df = pandas.DataFrame(columns=["ID","dist"])
    for i, pair in enumerate(dist_pairs):
        dist_df.loc[i] = [pair.split(',')[0], float(pair.split(',')[1])]

    dist_df.sort_values(by=["dist"], ascending=False).reset_index()
    gos = pandas.DataFrame(columns=["GO","dist","k","score0","score1","score2"])

    for j in range(0,len(dist_df.index)):
        if dist_df.loc[j,"dist"] == 0.0:
            # skip if 1NN is itself
            continue
        current_gos = label_df[label_df["ID"] == dist_df.loc[j,"ID"]]["GO"].values
        current_score0 = [1.0/dist_df.loc[j,"dist"]]
        current_score1 = [numpy.log(1.0/dist_df.loc[j,"dist"])]
        current_score2 = [numpy.sqrt(1.0/dist_df.loc[j,"dist"])]
        new_rows = pandas.DataFrame({"GO": current_gos,
                                     "dist": dist_df.loc[j,"dist"],
                                     "k": j,
                                     "score0": current_score0*len(current_gos),
                                     "score1": current_score1*len(current_gos),
                                     "score2": current_score2*len(current_gos)})
        gos = gos.append(new_rows)

    # ID,GO,score,formula,mode
    all_list = [[],[],[],[],[]]
    ID = knn_df.loc[ind,'ID']

    # dist mode
    # for threshold in numpy.arange(0.01,stop=0.105,step=0.01): #CA
    for threshold in numpy.arange(0.0005,stop=0.00101,step=0.0001): #PCA
        current_gos = gos[gos["dist"] <= threshold]
        if len(current_gos.index) == 0:
            current_gos = gos[gos["dist"] == gos["dist"].min()]
        current_gos_sta = current_gos.groupby("GO").sum().reset_index()
        current_gos_sta['score0'] = current_gos_sta['score0']/current_gos_sta['score0'].max()
        current_gos_sta['score1'] = current_gos_sta['score1']/current_gos_sta['score1'].max()
        current_gos_sta['score2'] = current_gos_sta['score2']/current_gos_sta['score2'].max()
        for k in range(0,len(current_gos_sta.index)):
            for formula in range(0,3):
                formula_str = 'score'+str(formula)
                all_list[0].append(ID)
                all_list[1].append(current_gos_sta.loc[k,'GO'])
                all_list[2].append(format(round(current_gos_sta.loc[k,formula_str],2),'.2f'))
                all_list[3].append(formula)
                all_list[4].append("d"+str(format(threshold,'.4f')).split('.')[1])


    # # k mode
    # k_list = [3,5,7,9,10,15,20,25]
    # for k in k_list:
    #     current_gos = gos[gos["k"] <= k]
    #     current_gos_sta = current_gos.groupby("GO").sum().reset_index()
    #     current_gos_sta['score0'] = current_gos_sta['score0']/current_gos_sta['score0'].max()
    #     current_gos_sta['score1'] = current_gos_sta['score1']/current_gos_sta['score1'].max()
    #     current_gos_sta['score2'] = current_gos_sta['score2']/current_gos_sta['score2'].max()
    #     for l in range(0,len(current_gos_sta.index)):
    #         for formula in range(0,3):
    #             formula_str = 'score'+str(formula)
    #             all_list[0].append(ID)
    #             all_list[1].append(current_gos_sta.loc[l,'GO'])
    #             all_list[2].append(format(round(current_gos_sta.loc[l,formula_str],2),'.2f'))
    #             all_list[3].append(formula)
    #             all_list[4].append("k"+str(k))

    return all_list

def write(m,f,cur_method):
    current_res_df = res_df[(res_df['mode']==m) & (res_df['formula']==f)].reset_index(drop=True)
    with open(args.output_folder + '/' + m + '_' + str(f), 'w') as f:
        f.write("AUTHOR TEAM_NAME\n")
        f.write("MODEL 1\n")
        f.write("KEYWORDS\t"+cur_method+"\n")
        for i in range(0,len(current_res_df.index)):
            f.write(current_res_df.loc[i,'ID'])
            f.write('\t')
            f.write(current_res_df.loc[i,'GO'])
            f.write('\t')
            f.write(current_res_df.loc[i,'score'])
            f.write('\n')
        f.write("END\n")
    return None

def vote_helper(args):
    return vote(*args)

def write_helper(args):
    return write(*args)

def main():

    global knn_df
    global label_df
    global res_df
    method = ['1/dist','log(1/dist)','sqrt(1/dist)']

    process_options()

    knn_df = pandas.read_csv(args.knn_file, sep='\t' ,header=0)
    label_df = pandas.read_csv(args.label_file, sep='\t' ,names=["ID","GO"])

    print "Unpred protein amount: %i" % len(knn_df[knn_df['pred_ID'].isnull()].index)
    knn_df = knn_df[-knn_df['pred_ID'].isnull()].reset_index(drop=True) #drop unpred protein

    pool = multiprocessing.Pool()
    vote_args = []

    for i in range(0,len(knn_df.index)):
    # for i in range(1,2):
        vote_args.append([i])

    p = multiprocessing.Pool()
    rs = p.map_async(vote_helper, vote_args)
    p.close() # No more work
    while (True):
      if (rs.ready()): break
      remaining = rs._number_left
      print "Waiting for", remaining, "tasks to complete..."
      time.sleep(2)

    res_df = pandas.DataFrame(columns=['ID','GO','score','formula','mode'])
    results = rs.get()
    for all_list in results:
        cur_df = pandas.DataFrame({'ID':all_list[0],
                                  'GO':all_list[1],
                                  'score':all_list[2],
                                  'formula':all_list[3],
                                  'mode':all_list[4]})
        res_df = res_df.append(cur_df)

    pool = multiprocessing.Pool()
    write_args = []

    for m in res_df['mode'].unique():
        for f, cur_method in enumerate(method):
            write_args.append([m,f,cur_method])

    p = multiprocessing.Pool()
    rs = p.map_async(write_helper, write_args)
    p.close() # No more work
    while (True):
      if (rs.ready()): break
      remaining = rs._number_left
      print "Waiting for", remaining, "tasks to complete..."
      time.sleep(2)

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
