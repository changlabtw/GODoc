import os
import sys
import time
import pandas
import matplotlib.pyplot as plt
import numpy as np

global function_file

def process_options(argv = sys.argv):
    global function_file

    if len(argv) < 2:
		print "Usage: %s function_file" % argv[0]
		sys.exit(1)

    function_file = argv[1]

    if not os.path.exists(function_file):
        print "function_file not found."
        sys.exit(1)

def main():

    process_options()

    function_df = pandas.read_csv(function_file, sep='\t', names=['ID','GO'])

    sta_go = function_df.groupby('GO').count().sort_values(['ID'],ascending=False)
    sta_go = sta_go.reset_index()
    sta_go['freq'] = sta_go['ID'] / float(len(function_df.index))
    sta_go['cum'] = 0
    bound = [0.68,0.95]
    bound_index = []
    current_bound = 0
    found = False
    for i in range(0,len(sta_go.index)):
        if i == 0:
            sta_go.loc[i,'cum'] = sta_go.loc[i,'freq']
        else:
            sta_go.loc[i,'cum'] = sta_go.loc[i,'freq'] + sta_go.loc[i-1,'cum']
            if sta_go.loc[i-1,'cum'] < bound[current_bound] and sta_go.loc[i,'cum'] > bound[current_bound]:
                found = True
            if found:
                if sta_go.loc[i-1,'ID'] != sta_go.loc[i,'ID']:
                    print "%i is at %f, count=%i." % (i,bound[current_bound],sta_go.loc[i-1,'ID'])
                    bound_index.append(i-1)
                    if current_bound <1:
                        current_bound += 1
                    found = False

    fig = sta_go['cum'].plot()
    fig.set_ylim([0,1])
    fig.set_title(os.path.basename(function_file).split('.')[0])
    fig.yaxis.set_ticks(np.arange(0, 1.01, 0.1))
    fig.annotate('68%,\n index=' + str(bound_index[0]) + ',\n count=' + str(sta_go['ID'][bound_index[0]]),
        (bound_index[0], sta_go['cum'][bound_index[0]]),
        xytext=(30, -60),
        textcoords='offset points',
        arrowprops=dict(arrowstyle='-|>'))
    fig.annotate('95%,\n index=' + str(bound_index[1]) + ',\n count=' + str(sta_go['ID'][bound_index[1]]),
        (bound_index[1], sta_go['cum'][bound_index[1]]),
        xytext=(30, -60),
        textcoords='offset points',
        arrowprops=dict(arrowstyle='-|>'))
    plt.savefig(os.path.basename(function_file).split('.')[0] + "_cum.png")

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s mins ---" % round(float((time.time() - start_time))/60, 2))
