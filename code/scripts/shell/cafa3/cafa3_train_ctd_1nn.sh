#!/bin/bash
for t in bpo cco mfo
do
  for fold in 0 1 2 3 4
  do
    python python/pca/pca_folder.py -i thesis/data/cafa3_train/ctd/ \
                                -l thesis/data/cafa3_train/nfold/$t/fold$fold/train_nr_ID.txt -list \
                                -o thesis/data/cafa3_train/nfold/$t/fold$fold/nr_pca.csv \
                                -om thesis/data/cafa3_train/nfold/$t/fold$fold/nr_pca_model.pkl
    python python/pca/pca_folder.py -i thesis/data/cafa3_train/ctd/ \
                                -l thesis/data/cafa3_train/nfold/$t/fold$fold/train_ID.txt -list \
                                -m thesis/data/cafa3_train/nfold/$t/fold$fold/nr_pca_model.pkl \
                                -o thesis/data/cafa3_train/nfold/$t/fold$fold/train_ctd_pca.csv
    python python/pca/pca_folder.py -i thesis/data/cafa3_train/ctd/ \
                                -l thesis/data/cafa3_train/nfold/$t/fold$fold/test_ID.txt -list \
                                -m thesis/data/cafa3_train/nfold/$t/fold$fold/nr_pca_model.pkl \
                                -o thesis/data/cafa3_train/nfold/$t/fold$fold/test_ctd_pca.csv
    nextflow oneNN.nf --train_vec thesis/data/cafa3_train/nfold/$t/fold$fold/train_ctd_pca.csv \
                      --train_label thesis/data/cafa3_train/nfold/$t/fold$fold/train_leaf.txt \
                      --test_vec thesis/data/cafa3_train/nfold/$t/fold$fold/test_ctd_pca.csv \
                      --cat $t \
                      --ont_db_path $PWD/data/go_20160601-termdb.obo \
                      --oa_file $PWD/thesis/data/cafa3_train/nfold/$t/fold$fold/test_pro.txt \
                      --benchmark $PWD/thesis/data/cafa3_train/nfold/$t/fold$fold/test_ID.txt \
                      --output thesis/data/cafa3_train/nfold/$t/fold$fold/ctd_1nn/
  done
done
