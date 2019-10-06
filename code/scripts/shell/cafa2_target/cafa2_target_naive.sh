#!/bin/bash
mkdir thesis/data/cafa2_target/naive
for t in bpo cco mfo
do
  for bt in 1 2
  do
    #naive_pred(matlab_path, cat, ont_db_path, oa_file, oa_train_file, benchmark_file, output_folder)
    matlab -nodisplay -r "addpath('./cafa2_eval/myscript');\
    naive_pred('./cafa2_eval/matlab','$t','./data/go_20130615-termdb.obo',\
    './thesis/data/cafa2_target/pro_$t.txt',\
    './thesis/data/cafa2_train/leaf_$t.txt',\
    './cafa2_eval/benchmark/lists/${t}_all_type${bt}.txt',\
    './thesis/data/cafa2_target/naive/${t}_type${bt}');quit;"
  done
done
