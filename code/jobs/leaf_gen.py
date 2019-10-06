import numpy as np

go_type = ['BPO','CCO','MFO']
threshold_list = np.arange(0.06, stop=0.21, step=0.02)
k_list = [3,5,7,9,10,15]
score_formula = [0,1,2]

for go in go_type:
    for formula in score_formula:
        for threshold in threshold_list:
            train_vec = "data/all_pred/all_" + go.lower() + "/train_vec.tsv"
            if go == 'BPO':
                train_label = "data/labels/all_function-P.tsv"
            elif go == 'CCO':
                train_label = "data/labels/all_function-C.tsv"
            elif go == 'MFO':
                train_label = "data/labels/all_function-F.tsv"
            test_vec = "data/all_pred/all_" + go.lower() + "/test_vec.tsv"
            output = "%s_d_%s_%i" % (go, format(round(threshold,2),'.2f').split('.')[1], formula)
            cmd = "leafScorePred.nf\ttype,%s,mode,d,train_vec,%s,train_label,%s,test_vec,%s,threshold,%s,score_formula,%s,output,%s" % (go, train_vec, train_label, test_vec, format(round(threshold,2),'.2f'), formula, output)
            print cmd

for go in go_type:
    for formula in score_formula:
        for k in k_list:
            train_vec = "data/all_" + go.lower() + "/train_vec.tsv"
            if go == 'BPO':
                train_label = "data/labels/all_function-P.tsv"
            elif go == 'CCO':
                train_label = "data/labels/all_function-C.tsv"
            elif go == 'MFO':
                train_label = "data/labels/all_function-F.tsv"
            test_vec = "data/all_" + go.lower() + "/test_vec.tsv"
            output = "%s_k_%i_%i" % (go, k, formula)
            cmd = "leafScorePred.nf\ttype,%s,mode,k,train_vec,%s,train_label,%s,test_vec,%s,k,%i,score_formula,%s,output,%s" % (go, train_vec, train_label, test_vec, k, formula, output)
            print cmd
