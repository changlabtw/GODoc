#!/bin/bash

for i in $(seq 1 20)
do
  mkdir tfpssm_exp/tfpssm_$i/nfold

  python python/pca/nfold_split.py -i tfpssm_exp/tfpssm_$i/bpo_pca_result.csv -n 5 -o tfpssm_exp/tfpssm_$i/nfold/bpo/
  python python/pca/nfold_split.py -i tfpssm_exp/tfpssm_$i/cco_pca_result.csv -n 5 -o tfpssm_exp/tfpssm_$i/nfold/cco/
  python python/pca/nfold_split.py -i tfpssm_exp/tfpssm_$i/mfo_pca_result.csv -n 5 -o tfpssm_exp/tfpssm_$i/nfold/mfo/
  for fold in $(seq 0 4)
  do
    #BPO
    cut -d, -f 1 tfpssm_exp/tfpssm_$i/nfold/bpo/fold${fold}/test_pca.csv > tfpssm_exp/tfpssm_$i/nfold/bpo/fold${fold}/test_ID_list.txt
    nextflow oneNN.nf --train_vec tfpssm_exp/tfpssm_$i/nfold/bpo/fold${fold}/train_pca.csv \
                      --train_label data/labels/all_function-P.tsv \
                      --test_vec tfpssm_exp/tfpssm_$i/nfold/bpo/fold${fold}/test_pca.csv \
                      --cat BPO \
                      --oa_file $PWD/data/pro_label/all_fun_pro_bpo.tsv \
                      --benchmark $PWD/tfpssm_exp/tfpssm_$i/nfold/bpo/fold${fold}/test_ID_list.txt \
                      --output tfpssm_exp/tfpssm_$i/nfold/bpo/fold${fold}

    #CCO
    cut -d, -f 1 tfpssm_exp/tfpssm_$i/nfold/cco/fold${fold}/test_pca.csv > tfpssm_exp/tfpssm_$i/nfold/cco/fold${fold}/test_ID_list.txt
    nextflow oneNN.nf --train_vec tfpssm_exp/tfpssm_$i/nfold/cco/fold${fold}/train_pca.csv \
                      --train_label data/labels/all_function-C.tsv \
                      --test_vec tfpssm_exp/tfpssm_$i/nfold/cco/fold${fold}/test_pca.csv \
                      --cat CCO \
                      --oa_file $PWD/data/pro_label/all_fun_pro_cco.tsv \
                      --benchmark $PWD/tfpssm_exp/tfpssm_$i/nfold/cco/fold${fold}/test_ID_list.txt \
                      --output tfpssm_exp/tfpssm_$i/nfold/cco/fold${fold}

    #MFO
    cut -d, -f 1 tfpssm_exp/tfpssm_$i/nfold/mfo/fold${fold}/test_pca.csv > tfpssm_exp/tfpssm_$i/nfold/mfo/fold${fold}/test_ID_list.txt
    nextflow oneNN.nf --train_vec tfpssm_exp/tfpssm_$i/nfold/mfo/fold${fold}/train_pca.csv \
                      --train_label data/labels/all_function-F.tsv \
                      --test_vec tfpssm_exp/tfpssm_$i/nfold/mfo/fold${fold}/test_pca.csv \
                      --cat MFO \
                      --oa_file $PWD/data/pro_label/all_fun_pro_mfo.tsv \
                      --benchmark $PWD/tfpssm_exp/tfpssm_$i/nfold/mfo/fold${fold}/test_ID_list.txt \
                      --output tfpssm_exp/tfpssm_$i/nfold/mfo/fold${fold}
  done
done
