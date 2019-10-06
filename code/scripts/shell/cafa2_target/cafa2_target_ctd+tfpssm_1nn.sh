#!/bin/bash
mkdir thesis/data/cafa2_target/ctd+tfpssm_1nn
for t in bpo cco mfo
do
  for bt in 1 2
  do
    mkdir thesis/data/cafa2_target/ctd+tfpssm_1nn/${t}_type${bt}/
    python python/vector/combine.py -v thesis/data/cafa2_target/tfpssm_1nn/${t}_type${bt}/train_tfpssm_pca.csv \
                                       thesis/data/cafa2_target/ctd_1nn/${t}_type${bt}/train_ctd_pca.csv \
                                    -o thesis/data/cafa2_target/ctd+tfpssm_1nn/${t}_type${bt}/train_ctd+tfpssm_pca.csv
    python python/vector/combine.py -v thesis/data/cafa2_target/tfpssm_1nn/${t}_type${bt}/test_tfpssm_pca.csv \
                                       thesis/data/cafa2_target/ctd_1nn/${t}_type${bt}/test_ctd_pca.csv \
                                    -o thesis/data/cafa2_target/ctd+tfpssm_1nn/${t}_type${bt}/test_ctd+tfpssm_pca.csv
    nextflow oneNN.nf --train_vec thesis/data/cafa2_target/ctd+tfpssm_1nn/${t}_type${bt}/train_ctd+tfpssm_pca.csv \
                      --train_label thesis/data/cafa2_train/leaf_$t.txt \
                      --test_vec thesis/data/cafa2_target/ctd+tfpssm_1nn/${t}_type${bt}/test_ctd+tfpssm_pca.csv \
                      --cat $t \
                      --ont_db_path $PWD/data/go_20130615-termdb.obo \
                      --oa_file $PWD/thesis/data/cafa2_target/pro_$t.txt \
                      --benchmark $PWD/cafa2_eval/benchmark/lists/${t}_all_type${bt}.txt \
                      --output thesis/data/cafa2_target/ctd+tfpssm_1nn/${t}_type${bt}/
  done
done
