#!/bin/bash
mkdir thesis/data/cafa2_target/ctd_pure_1nn
for t in bpo cco mfo
do
  for bt in 1 2
  do
    mkdir thesis/data/cafa2_target/ctd_pure_1nn/${t}_type${bt}
    python python/vector/vector_merge.py -i thesis/data/cafa2_train/ctd/ \
                                         -l thesis/data/cafa2_train/ID_$t.txt -list \
                                         -o thesis/data/cafa2_target/ctd_pure_1nn/${t}_type${bt}/train_ctd.csv
    python python/vector/vector_merge.py -i thesis/data/cafa2_target/ctd/ \
                                         -l thesis/data/cafa2_target/ID_$t.txt -list \
                                         -o thesis/data/cafa2_target/ctd_pure_1nn/${t}_type${bt}/test_ctd.csv
    nextflow oneNN.nf --train_vec thesis/data/cafa2_target/ctd_pure_1nn/${t}_type${bt}/train_ctd.csv \
                      --train_label thesis/data/cafa2_train/leaf_$t.txt \
                      --test_vec thesis/data/cafa2_target/ctd_pure_1nn/${t}_type${bt}/test_ctd.csv \
                      --cat $t \
                      --ont_db_path $PWD/data/go_20130615-termdb.obo \
                      --oa_file $PWD/thesis/data/cafa2_target/pro_$t.txt \
                      --benchmark $PWD/cafa2_eval/benchmark/lists/${t}_all_type${bt}.txt \
                      --output thesis/data/cafa2_target/ctd_pure_1nn/${t}_type${bt}/
  done
done
