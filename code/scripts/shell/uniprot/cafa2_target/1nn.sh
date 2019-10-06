#!/bin/bash
#PCA whiten and non redundant training data for SVD explained variance ratio=0.975
cur_path=exp/test
mkdir ${cur_path}
for t in cco
do
  for bt in 1
  do
    # python python/pca/pca_folder.py -i thesis/data/uniprot/cafa2_train/tfpssm/ -w -n 0.975 \
    #                             -l thesis/data/uniprot/cafa2_train/ID_$t.txt -list \
    #                             -om ${cur_path}/pca_model.pkl \
    #                             -o ${cur_path}/train_tfpssm_pca.csv
    python python/pca/pca_folder.py -i thesis/data/uniprot/cafa2_target/tfpssm/ -w -n 0.975 \
                                -l thesis/data/uniprot/cafa2_target/ID_$t.txt -list \
                                -m ${cur_path}/pca_model.pkl \
                                -o ${cur_path}/test_tfpssm_pca.csv
    nextflow oneNN.nf --train_vec ${cur_path}/train_tfpssm_pca.csv \
                      --train_label thesis/data/uniprot/cafa2_train/leaf_$t.txt \
                      --test_vec ${cur_path}/test_tfpssm_pca.csv \
                      --cat $t \
                      --ont_db_path $PWD/data/go_20130615-termdb.obo \
                      --oa_file $PWD/thesis/data/uniprot/cafa2_target/pro_$t.txt \
                      --benchmark $PWD/cafa2_eval/benchmark/lists/${t}_all_type${bt}.txt \
                      --output ${cur_path}/
  done
done
