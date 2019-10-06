#!/bin/bash
for t in bpo cco mfo
do
  for fold in 0 1 2 3 4
  do
    python python/vector/combine.py -v thesis/data/cafa3_train/nfold/$t/fold$fold/train_tfpssm_pca.csv \
                                       thesis/data/cafa3_train/nfold/$t/fold$fold/train_ctd_pca.csv \
                                    -o thesis/data/cafa3_train/nfold/$t/fold$fold/train_ctd+tfpssm_pca.csv
    python python/vector/combine.py -v thesis/data/cafa3_train/nfold/$t/fold$fold/test_tfpssm_pca.csv \
                                       thesis/data/cafa3_train/nfold/$t/fold$fold/test_ctd_pca.csv \
                                    -o thesis/data/cafa3_train/nfold/$t/fold$fold/test_ctd+tfpssm_pca.csv
    nextflow oneNN.nf --train_vec thesis/data/cafa3_train/nfold/$t/fold$fold/train_ctd+tfpssm_pca.csv \
                      --train_label thesis/data/cafa3_train/nfold/$t/fold$fold/train_leaf.txt \
                      --test_vec thesis/data/cafa3_train/nfold/$t/fold$fold/test_ctd+tfpssm_pca.csv \
                      --cat $t \
                      --ont_db_path $PWD/data/go_20160601-termdb.obo \
                      --oa_file $PWD/thesis/data/cafa3_train/nfold/$t/fold$fold/test_pro.txt \
                      --benchmark $PWD/thesis/data/cafa3_train/nfold/$t/fold$fold/test_ID.txt \
                      --output thesis/data/cafa3_train/nfold/$t/fold$fold/ctd+tfpssm_1nn/
  done
done
