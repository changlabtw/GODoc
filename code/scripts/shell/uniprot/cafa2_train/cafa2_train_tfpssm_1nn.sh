#!/bin/bash
for t in cco mfo bpo
do
  for fold in 0 1 2 3 4
  do
    python python/pca/pca_folder.py -i thesis/data/uniprot/cafa2_train/tfpssm/ \
                                -l thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/train_nr_ID.txt -list \
                                -o thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/nr_pca.csv \
                                -om thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/nr_pca_model.pkl
    python python/pca/pca_folder.py -i thesis/data/uniprot/cafa2_train/tfpssm/ \
                                -l thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/train_ID.txt -list \
                                -m thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/nr_pca_model.pkl \
                                -o thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/train_tfpssm_pca.csv
    python python/pca/pca_folder.py -i thesis/data/uniprot/cafa2_train/tfpssm/ \
                                -l thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/test_ID.txt -list \
                                -m thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/nr_pca_model.pkl \
                                -o thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/test_tfpssm_pca.csv
    nextflow oneNN.nf --train_vec thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/train_tfpssm_pca.csv \
                      --train_label thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/train_leaf.txt \
                      --test_vec thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/test_tfpssm_pca.csv \
                      --cat $t \
                      --ont_db_path $PWD/data/go_20130615-termdb.obo \
                      --oa_file $PWD/thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/test_pro.txt \
                      --benchmark $PWD/thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/test_ID.txt \
                      --output thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/tfpssm_1nn/
  done
done
