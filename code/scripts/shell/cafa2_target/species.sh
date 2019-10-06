#!/bin/bash
# for t in bpo cco mfo
for t in cco
do
  for p in 75
  do
    for sp in eukarya prokarya
    do
      for bt in 1
      do
        # seq_eval(matlab_path, cat, ont_db_path, oa_file, pred_file, benchmark_file, output_folder)
        # tfpssm 1nn
        nextflow oneNN.nf --train_vec thesis/data/cafa2_target/tfpssm_1nn/${t}_type${bt}/train_tfpssm_pca.csv \
                          --train_label thesis/data/cafa2_train/leaf_$t.txt \
                          --test_vec thesis/data/cafa2_target/tfpssm_1nn/${t}_type${bt}/test_tfpssm_pca.csv \
                          --cat $t \
                          --ont_db_path $PWD/data/go_20130615-termdb.obo \
                          --oa_file $PWD/thesis/data/cafa2_target/pro_$t.txt \
                          --benchmark $PWD/cafa2_eval/benchmark/lists/${t}_${sp}_type${bt}.txt \
                          --output thesis/data/cafa2_target/tfpssm_1nn/${t}_type${bt}_${sp}/
        # tfpssm vote
        mkdir thesis/data/cafa2_target/pro_vote/${t}_type${bt}_${sp}
        mkdir thesis/data/cafa2_target/pro_vote/${t}_type${bt}_${sp}/${p}
        matlab -nodisplay -r "addpath('./cafa2_eval/myscript');\
        seq_eval('./cafa2_eval/matlab','$t','./data/go_20130615-termdb.obo',\
        './thesis/data/cafa2_target/pro_$t.txt',\
        './thesis/data/cafa2_target/pro_vote/${t}_type${bt}/${p}/vote_score.tsv',\
        './cafa2_eval/benchmark/lists/${t}_${sp}_type${bt}.txt',\
        './thesis/data/cafa2_target/pro_vote/${t}_type${bt}_${sp}/${p}');quit;"
        # cath vote
        # mkdir thesis/data/cafa2_target/pro_cathvote/${t}_type${bt}_${sp}
        # mkdir thesis/data/cafa2_target/pro_cathvote/${t}_type${bt}_${sp}/${p}
        # matlab -nodisplay -r "addpath('./cafa2_eval/myscript');\
        # seq_eval('./cafa2_eval/matlab','$t','./data/go_20130615-termdb.obo',\
        # './thesis/data/cafa2_target/pro_$t.txt',\
        # './thesis/data/cafa2_target/pro_cathvote/${t}_type${bt}/${p}/cathvote_score.tsv',\
        # './cafa2_eval/benchmark/lists/${t}_${sp}_type${bt}.txt',\
        # './thesis/data/cafa2_target/pro_cathvote/${t}_type${bt}_${sp}/${p}');quit;"
      done
    done
  done
done
