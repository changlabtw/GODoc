#!/bin/bash

for i in $(seq 21 30)
do
  nextflow blastToTfpssm.nf --query data/swiss/psiBlastResult --output data/swiss/tfpssm_exp/tfpssm_$i/ --d $i

  mkdir cafa3_train/tfpssm_$i
  python python/pca/pca_folder.py -i data/swiss/tfpssm_exp/tfpssm_$i/ -a -o cafa3_train/tfpssm_$i/pca_result.csv -om cafa3_train/tfpssm_$i/pca_model.pkl

  python python/pca/filter.py -i cafa3_train/tfpssm_$i/pca_result.csv -l data/labels/cafa3_bpo_list.txt -o cafa3_train/tfpssm_$i/bpo_pca_result.csv
  python python/pca/filter.py -i cafa3_train/tfpssm_$i/pca_result.csv -l data/labels/cafa3_cco_list.txt -o cafa3_train/tfpssm_$i/cco_pca_result.csv
  python python/pca/filter.py -i cafa3_train/tfpssm_$i/pca_result.csv -l data/labels/cafa3_mfo_list.txt -o cafa3_train/tfpssm_$i/mfo_pca_result.csv

  mkdir cafa3_train/tfpssm_$i/nfold

  python python/pca/nfold_split.py -i cafa3_train/tfpssm_$i/bpo_pca_result.csv -n 5 -o cafa3_train/tfpssm_$i/nfold/bpo/
  python python/pca/nfold_split.py -i cafa3_train/tfpssm_$i/cco_pca_result.csv -n 5 -o cafa3_train/tfpssm_$i/nfold/cco/
  python python/pca/nfold_split.py -i cafa3_train/tfpssm_$i/mfo_pca_result.csv -n 5 -o cafa3_train/tfpssm_$i/nfold/mfo/
  for fold in $(seq 0 4)
  do
    #BPO
    cut -d, -f 1 cafa3_train/tfpssm_$i/nfold/bpo/fold${fold}/test_pca.csv > cafa3_train/tfpssm_$i/nfold/bpo/fold${fold}/test_ID_list.txt
    nextflow oneNN.nf --train_vec cafa3_train/tfpssm_$i/nfold/bpo/fold${fold}/train_pca.csv \
                      --train_label data/labels/cafa3_function-P.tsv \
                      --test_vec cafa3_train/tfpssm_$i/nfold/bpo/fold${fold}/test_pca.csv \
                      --cat BPO \
                      --oa_file $PWD/data/pro_label/cafa3_fun_pro_bpo.tsv \
                      --benchmark $PWD/cafa3_train/tfpssm_$i/nfold/bpo/fold${fold}/test_ID_list.txt \
                      --output cafa3_train/tfpssm_$i/nfold/bpo/fold${fold}

    #CCO
    cut -d, -f 1 cafa3_train/tfpssm_$i/nfold/cco/fold${fold}/test_pca.csv > cafa3_train/tfpssm_$i/nfold/cco/fold${fold}/test_ID_list.txt
    nextflow oneNN.nf --train_vec cafa3_train/tfpssm_$i/nfold/cco/fold${fold}/train_pca.csv \
                      --train_label data/labels/cafa3_function-C.tsv \
                      --test_vec cafa3_train/tfpssm_$i/nfold/cco/fold${fold}/test_pca.csv \
                      --cat CCO \
                      --oa_file $PWD/data/pro_label/cafa3_fun_pro_cco.tsv \
                      --benchmark $PWD/cafa3_train/tfpssm_$i/nfold/cco/fold${fold}/test_ID_list.txt \
                      --output cafa3_train/tfpssm_$i/nfold/cco/fold${fold}

    #MFO
    cut -d, -f 1 cafa3_train/tfpssm_$i/nfold/mfo/fold${fold}/test_pca.csv > cafa3_train/tfpssm_$i/nfold/mfo/fold${fold}/test_ID_list.txt
    nextflow oneNN.nf --train_vec cafa3_train/tfpssm_$i/nfold/mfo/fold${fold}/train_pca.csv \
                      --train_label data/labels/cafa3_function-F.tsv \
                      --test_vec cafa3_train/tfpssm_$i/nfold/mfo/fold${fold}/test_pca.csv \
                      --cat MFO \
                      --oa_file $PWD/data/pro_label/cafa3_fun_pro_mfo.tsv \
                      --benchmark $PWD/cafa3_train/tfpssm_$i/nfold/mfo/fold${fold}/test_ID_list.txt \
                      --output cafa3_train/tfpssm_$i/nfold/mfo/fold${fold}
  done
done
