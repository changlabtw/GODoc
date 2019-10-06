#!/bin/bash
for t in bpo cco mfo
do
  for fold in 0 1 2 3 4
  do
    python python/vector/vector_merge.py -i thesis/data/cafa2_train/ctd/ \
                                         -l thesis/data/cafa2_train/nfold/$t/fold$fold/train_ID.txt -list \
                                         -o thesis/data/cafa2_train/nfold/$t/fold$fold/train_ctd.csv
    python python/vector/vector_merge.py -i thesis/data/cafa2_train/ctd/ \
                                         -l thesis/data/cafa2_train/nfold/$t/fold$fold/test_ID.txt -list \
                                         -o thesis/data/cafa2_train/nfold/$t/fold$fold/test_ctd.csv
    nextflow oneNN.nf --train_vec thesis/data/cafa2_train/nfold/$t/fold$fold/train_ctd.csv \
                      --train_label thesis/data/cafa2_train/nfold/$t/fold$fold/train_leaf.txt \
                      --test_vec thesis/data/cafa2_train/nfold/$t/fold$fold/test_ctd.csv \
                      --cat $t \
                      --ont_db_path $PWD/data/go_20130615-termdb.obo \
                      --oa_file $PWD/thesis/data/cafa2_train/nfold/$t/fold$fold/test_pro.txt \
                      --benchmark $PWD/thesis/data/cafa2_train/nfold/$t/fold$fold/test_ID.txt \
                      --output thesis/data/cafa2_train/nfold/$t/fold$fold/ctd_pure_1nn/
  done
done
