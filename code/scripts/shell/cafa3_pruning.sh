#!/bin/bash

for i in 3
do
  for fold in $(seq 0 4)
  do
    for thres in $(seq 0.05 0.01 0.3)
    do
      #BPO
      python python/pruning/pruning.py -i cafa3_train/tfpssm_${i}/nfold/bpo/fold${fold}/pro_score.txt -r cafa3_train/tfpssm_${i}/nfold/bpo/pruning_ratio.tsv -t ${thres} -o cafa3_train/tfpssm_${i}/nfold/bpo/fold${fold}/pruning_${thres}_score.txt
      matlab -nodisplay -r "addpath('./cafa2_eval/myscript');fmax('./cafa2_eval/matlab','BPO','./cafa2_eval/ontology/', \
      'data/pro_label/cafa3_fun_pro_bpo.tsv','cafa3_train/tfpssm_${i}/nfold/bpo/fold${fold}/pruning_${thres}_score.txt', \
      'cafa3_train/tfpssm_$i/nfold/bpo/fold${fold}/test_ID_list.txt','cafa3_train/tfpssm_${i}/nfold/bpo/fold${fold}/pruning_${thres}_res.txt');quit;"

      #CCO
      python python/pruning/pruning.py -i cafa3_train/tfpssm_${i}/nfold/cco/fold${fold}/pro_score.txt -r cafa3_train/tfpssm_${i}/nfold/cco/pruning_ratio.tsv -t ${thres} -o cafa3_train/tfpssm_${i}/nfold/cco/fold${fold}/pruning_${thres}_score.txt
      matlab -nodisplay -r "addpath('./cafa2_eval/myscript');fmax('./cafa2_eval/matlab','CCO','./cafa2_eval/ontology/', \
      'data/pro_label/cafa3_fun_pro_cco.tsv','cafa3_train/tfpssm_${i}/nfold/cco/fold${fold}/pruning_${thres}_score.txt', \
      'cafa3_train/tfpssm_$i/nfold/cco/fold${fold}/test_ID_list.txt','cafa3_train/tfpssm_${i}/nfold/cco/fold${fold}/pruning_${thres}_res.txt');quit;"

      #MFO
      python python/pruning/pruning.py -i cafa3_train/tfpssm_${i}/nfold/mfo/fold${fold}/pro_score.txt -r cafa3_train/tfpssm_${i}/nfold/mfo/pruning_ratio.tsv -t ${thres} -o cafa3_train/tfpssm_${i}/nfold/mfo/fold${fold}/pruning_${thres}_score.txt
      matlab -nodisplay -r "addpath('./cafa2_eval/myscript');fmax('./cafa2_eval/matlab','MFO','./cafa2_eval/ontology/', \
      'data/pro_label/cafa3_fun_pro_mfo.tsv','cafa3_train/tfpssm_${i}/nfold/mfo/fold${fold}/pruning_${thres}_score.txt', \
      'cafa3_train/tfpssm_$i/nfold/mfo/fold${fold}/test_ID_list.txt','cafa3_train/tfpssm_${i}/nfold/mfo/fold${fold}/pruning_${thres}_res.txt');quit;"
    done
  done
done
