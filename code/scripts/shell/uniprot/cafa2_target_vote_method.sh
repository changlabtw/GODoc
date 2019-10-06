#!/bin/bash
for t in cco
do
  for p in 75
  do
    for method in 1 2
    do
      for bt in 1
      do
        mkdir thesis/data/uniprot/cafa2_target/pro_vote
        mkdir thesis/data/uniprot/cafa2_target/pro_vote/${t}_type${bt}
        mkdir thesis/data/uniprot/cafa2_target/pro_vote/${t}_type${bt}/${p}_${method}
        python python/leafVote/leafVote.py -i thesis/data/uniprot/cafa2_target/knn_${t}_${p}_res.tsv \
                                           -l thesis/data/uniprot/cafa2_train/pro_${t}.txt \
                                           -s ${method} -o thesis/data/uniprot/cafa2_target/pro_vote/${t}_type${bt}/${p}_${method}/vote_score.tsv
        # seq_eval(matlab_path, cat, ont_db_path, oa_file, pred_file, benchmark_file, output_folder)
        matlab -nodisplay -r "addpath('./cafa2_eval/myscript');\
        seq_eval('./cafa2_eval/matlab','$t','./data/go_20130615-termdb.obo',\
        './thesis/data/uniprot/cafa2_target/pro_$t.txt',\
        './thesis/data/uniprot/cafa2_target/pro_vote/${t}_type${bt}/${p}_${method}/vote_score.tsv',\
        './cafa2_eval/benchmark/lists/${t}_all_type${bt}.txt',\
        './thesis/data/uniprot/cafa2_target/pro_vote/${t}_type${bt}/${p}_${method}');quit;"
      done
    done
  done
done
