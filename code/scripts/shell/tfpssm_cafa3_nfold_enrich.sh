#!/bin/bash

for i in $(seq 1 20)
do
  for fold in $(seq 0 4)
  do
    #BPO
    python python/gorelation/enrich.py -i cafa3_train/tfpssm_${i}/nfold/bpo/fold${fold}/pro_score.txt -r python/gorelation/cafa3_bpo_rel.tsv -o cafa3_train/tfpssm_${i}/nfold/bpo/fold${fold}/enrich_score.txt
    matlab -nodisplay -r "addpath('./cafa2_eval/myscript');fmax('./cafa2_eval/matlab','BPO','./cafa2_eval/ontology/', \
    'data/pro_label/cafa3_fun_pro_bpo.tsv','cafa3_train/tfpssm_${i}/nfold/bpo/fold${fold}/enrich_score.txt', \
    'cafa3_train/tfpssm_$i/nfold/bpo/fold${fold}/test_ID_list.txt','cafa3_train/tfpssm_${i}/nfold/bpo/fold${fold}/enrich_res.txt');quit;"

    #CCO
    python python/gorelation/enrich.py -i cafa3_train/tfpssm_${i}/nfold/cco/fold${fold}/pro_score.txt -r python/gorelation/cafa3_cco_rel.tsv -o cafa3_train/tfpssm_${i}/nfold/cco/fold${fold}/enrich_score.txt
    matlab -nodisplay -r "addpath('./cafa2_eval/myscript');fmax('./cafa2_eval/matlab','CCO','./cafa2_eval/ontology/', \
    'data/pro_label/cafa3_fun_pro_cco.tsv','cafa3_train/tfpssm_${i}/nfold/cco/fold${fold}/enrich_score.txt', \
    'cafa3_train/tfpssm_$i/nfold/cco/fold${fold}/test_ID_list.txt','cafa3_train/tfpssm_${i}/nfold/cco/fold${fold}/enrich_res.txt');quit;"

    #MFO
    python python/gorelation/enrich.py -i cafa3_train/tfpssm_${i}/nfold/mfo/fold${fold}/pro_score.txt -r python/gorelation/cafa3_mfo_rel.tsv -o cafa3_train/tfpssm_${i}/nfold/mfo/fold${fold}/enrich_score.txt
    matlab -nodisplay -r "addpath('./cafa2_eval/myscript');fmax('./cafa2_eval/matlab','MFO','./cafa2_eval/ontology/', \
    'data/pro_label/cafa3_fun_pro_mfo.tsv','cafa3_train/tfpssm_${i}/nfold/mfo/fold${fold}/enrich_score.txt', \
    'cafa3_train/tfpssm_$i/nfold/mfo/fold${fold}/test_ID_list.txt','cafa3_train/tfpssm_${i}/nfold/mfo/fold${fold}/enrich_res.txt');quit;"
  done
done
