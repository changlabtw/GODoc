#!/bin/bash

for t in cco mfo bpo
do
  for fold in 0 1 2 3 4
  do
    #naive_pred(matlab_path, cat, ont_db_path, oa_file, oa_train_file, benchmark_file, output_folder)
    matlab -nodisplay -r "addpath('./cafa2_eval/myscript');\
    naive_pred('./cafa2_eval/matlab','$t','./data/go_20130615-termdb.obo',\
    './thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/test_pro.txt',\
    './thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/train_leaf.txt',\
    './thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/test_ID.txt',\
    './thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/naive_leaf');quit;"
    matlab -nodisplay -r "addpath('./cafa2_eval/myscript');\
    naive_pred('./cafa2_eval/matlab','$t','./data/go_20130615-termdb.obo',\
    './thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/test_pro.txt',\
    './thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/train_pro.txt',\
    './thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/test_ID.txt',\
    './thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/naive_pro');quit;"
  done
done
