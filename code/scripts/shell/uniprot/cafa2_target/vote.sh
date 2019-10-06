#!/bin/bash
cur_path=exp/vote_3_25
vec_path=exp/1nn
mkdir ${cur_path}
for t in cco
do
  for p in 25
  do
    python python/knn/dynamic_knn.py -b ${vec_path}/train_tfpssm_pca.csv -k 3\
                                     -train ${vec_path}/train_tfpssm_pca.csv \
                                     -test ${vec_path}/test_tfpssm_pca.csv \
                                     -t ${p}% -o ${cur_path}/knn_${t}_${p}_res.tsv
    for lt in pro
    do
      for bt in 1
      do
        python python/leafVote/leafVote.py -i ${cur_path}/knn_${t}_${p}_res.tsv \
                                           -l thesis/data/uniprot/cafa2_train/${lt}_${t}.txt \
                                           -s 0 -o ${cur_path}/vote_score.tsv
        # seq_eval(matlab_path, cat, ont_db_path, oa_file, pred_file, benchmark_file, output_folder)
        matlab -nodisplay -r "addpath('./cafa2_eval/myscript');\
        seq_eval('./cafa2_eval/matlab','$t','./data/go_20130615-termdb.obo',\
        './thesis/data/uniprot/cafa2_target/pro_$t.txt',\
        '${cur_path}/vote_score.tsv',\
        './cafa2_eval/benchmark/lists/${t}_all_type${bt}.txt',\
        '${cur_path}');quit;"
      done
    done
  done
done
