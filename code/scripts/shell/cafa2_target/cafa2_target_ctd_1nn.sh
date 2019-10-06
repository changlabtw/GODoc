#!/bin/bash
mkdir thesis/data/cafa2_target/ctd_1nn
for t in bpo cco mfo
do
  for bt in 1 2
  do
    mkdir thesis/data/cafa2_target/ctd_1nn/${t}_type${bt}
    python python/pca/pca_folder.py -i thesis/data/cafa2_train/ctd/ \
                                -l thesis/data/cafa2_train/cafa2_train_nr_ID.txt -list \
                                -o thesis/data/cafa2_target/ctd_1nn/${t}_type${bt}/cafa2_train_nr_pca.csv \
                                -om thesis/data/cafa2_target/ctd_1nn/${t}_type${bt}/nr_pca_model.pkl
    python python/pca/pca_folder.py -i thesis/data/cafa2_train/ctd/ \
                                -l thesis/data/cafa2_train/ID_$t.txt -list \
                                -m thesis/data/cafa2_target/ctd_1nn/${t}_type${bt}/nr_pca_model.pkl \
                                -o thesis/data/cafa2_target/ctd_1nn/${t}_type${bt}/train_ctd_pca.csv
    python python/pca/pca_folder.py -i thesis/data/cafa2_target/ctd/ \
                                -l thesis/data/cafa2_target/ID_$t.txt -list \
                                -m thesis/data/cafa2_target/ctd_1nn/${t}_type${bt}/nr_pca_model.pkl \
                                -o thesis/data/cafa2_target/ctd_1nn/${t}_type${bt}/test_ctd_pca.csv
    nextflow oneNN.nf --train_vec thesis/data/cafa2_target/ctd_1nn/${t}_type${bt}/train_ctd_pca.csv \
                      --train_label thesis/data/cafa2_train/leaf_$t.txt \
                      --test_vec thesis/data/cafa2_target/ctd_1nn/${t}_type${bt}/test_ctd_pca.csv \
                      --cat $t \
                      --ont_db_path $PWD/data/go_20130615-termdb.obo \
                      --oa_file $PWD/thesis/data/cafa2_target/pro_$t.txt \
                      --benchmark $PWD/cafa2_eval/benchmark/lists/${t}_all_type${bt}.txt \
                      --output thesis/data/cafa2_target/ctd_1nn/${t}_type${bt}/
  done
done
