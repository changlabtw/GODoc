#!/bin/bash
for fold in $(seq 0 4)
do

  # python python/knn/dynamic_knn.py -b cafa3_train/tfpssm_13/pca_result.csv -train cafa3_train/tfpssm_13/nfold/cco/fold${fold}/train_pca.csv -test cafa3_train/tfpssm_13/nfold/cco/fold${fold}/test_pca.csv -t 75% -o cafa3_train/tfpssm_13/nfold/cco/fold${fold}/cco_knn.tsv
  # #CCO
  # python python/cath/ff_filter.py -i cafa3_train/tfpssm_13/nfold/cco/fold${fold}/cco_knn.tsv -test_m cafa3/cath/cafa3_train_ff_ind.pkl -train_m cafa3/cath/cafa3_train_ff_ind.pkl -o cafa3_train/tfpssm_13/nfold/cco/fold${fold}/cco_knn_filtered_res.tsv
  # #leaf
  # python python/cath/cath_vote_multi.py -i cafa3_train/tfpssm_13/nfold/cco/fold${fold}/cco_knn_filtered_res.tsv -l data/labels/cafa3_function-C.tsv -m 2 -o cafa3_train/tfpssm_13/nfold/cco/fold${fold}/cath_vote.txt
  # # matlab -nodisplay -r "addpath('./cafa2_eval/myscript');fmax_new('./cafa2_eval/matlab','CCO','./data/go-basic.obo','./data/pro_label/cafa3_fun_pro_cco.tsv','cafa3_train/tfpssm_13/nfold/cco/fold${fold}/cath_vote.txt','./cafa3_train/tfpssm_13/nfold/cco/fold${fold}/test_ID_list.txt','./cafa3_train/tfpssm_13/nfold/cco/fold${fold}/cath_vote_res.txt');quit;"
  # #enrich at leaf
  # python python/gorelation/enrich.py -i cafa3_train/tfpssm_13/nfold/cco/fold${fold}/cath_vote.txt -r python/gorelation/cafa3_cco_rel.tsv -o cafa3_train/tfpssm_13/nfold/cco/fold${fold}/cath_vote_enrich.txt
  # matlab -nodisplay -r "addpath('./cafa2_eval/myscript');fmax_new('./cafa2_eval/matlab','CCO','./data/go-basic.obo','./data/pro_label/cafa3_fun_pro_cco.tsv','cafa3_train/tfpssm_13/nfold/cco/fold${fold}/cath_vote_enrich.txt','./cafa3_train/tfpssm_13/nfold/cco/fold${fold}/test_ID_list.txt','./cafa3_train/tfpssm_13/nfold/cco/fold${fold}/cath_vote_enrich_res.txt');quit;"
  # #pro
  # python python/cath/cath_vote_multi.py -i cafa3_train/tfpssm_13/nfold/cco/fold${fold}/cco_knn_filtered_res.tsv -l data/pro_label/cafa3_fun_pro_cco.tsv -m 2 -o cafa3_train/tfpssm_13/nfold/cco/fold${fold}/cath_vote_pro.txt
  # # matlab -nodisplay -r "addpath('./cafa2_eval/myscript');fmax_new('./cafa2_eval/matlab','CCO','./data/go-basic.obo','./data/pro_label/cafa3_fun_pro_cco.tsv','cafa3_train/tfpssm_13/nfold/cco/fold${fold}/cath_vote_pro.txt','./cafa3_train/tfpssm_13/nfold/cco/fold${fold}/test_ID_list.txt','./cafa3_train/tfpssm_13/nfold/cco/fold${fold}/cath_vote_pro_res.txt');quit;"
  # #enrich at pro
  # python python/gorelation/enrich.py -i cafa3_train/tfpssm_13/nfold/cco/fold${fold}/cath_vote_pro.txt -r python/gorelation/cafa3_cco_rel.tsv -o cafa3_train/tfpssm_13/nfold/cco/fold${fold}/cath_vote_pro_enrich.txt
  # # matlab -nodisplay -r "addpath('./cafa2_eval/myscript');fmax_new('./cafa2_eval/matlab','CCO','./data/go-basic.obo','./data/pro_label/cafa3_fun_pro_cco.tsv','cafa3_train/tfpssm_13/nfold/cco/fold${fold}/cath_vote_pro_enrich.txt','./cafa3_train/tfpssm_13/nfold/cco/fold${fold}/test_ID_list.txt','./cafa3_train/tfpssm_13/nfold/cco/fold${fold}/cath_vote_pro_enrich_res.txt');quit;"
  #
  # #cath_vote_multi method 0
  # #leaf
  # python python/cath/cath_vote_multi.py -i cafa3_train/tfpssm_13/nfold/cco/fold${fold}/cco_knn_filtered_res.tsv -l data/labels/cafa3_function-C.tsv -m 0 -o cafa3_train/tfpssm_13/nfold/cco/fold${fold}/cath_vote_m0.txt
  # matlab -nodisplay -r "addpath('./cafa2_eval/myscript');fmax_new('./cafa2_eval/matlab','CCO','./data/go-basic.obo','./data/pro_label/cafa3_fun_pro_cco.tsv','cafa3_train/tfpssm_13/nfold/cco/fold${fold}/cath_vote_m0.txt','./cafa3_train/tfpssm_13/nfold/cco/fold${fold}/test_ID_list.txt','./cafa3_train/tfpssm_13/nfold/cco/fold${fold}/cath_vote_m0_res.txt');quit;"
  # #enrich at leaf
  # python python/gorelation/enrich.py -i cafa3_train/tfpssm_13/nfold/cco/fold${fold}/cath_vote_m0.txt -r python/gorelation/cafa3_cco_rel.tsv -o cafa3_train/tfpssm_13/nfold/cco/fold${fold}/cath_vote_m0_enrich.txt
  # matlab -nodisplay -r "addpath('./cafa2_eval/myscript');fmax_new('./cafa2_eval/matlab','CCO','./data/go-basic.obo','./data/pro_label/cafa3_fun_pro_cco.tsv','cafa3_train/tfpssm_13/nfold/cco/fold${fold}/cath_vote_m0_enrich.txt','./cafa3_train/tfpssm_13/nfold/cco/fold${fold}/test_ID_list.txt','./cafa3_train/tfpssm_13/nfold/cco/fold${fold}/cath_vote_m0_enrich_res.txt');quit;"
  # #pro
  # python python/cath/cath_vote_multi.py -i cafa3_train/tfpssm_13/nfold/cco/fold${fold}/cco_knn_filtered_res.tsv -l data/pro_label/cafa3_fun_pro_cco.tsv -m 0 -o cafa3_train/tfpssm_13/nfold/cco/fold${fold}/cath_vote_pro_m0.txt
  # matlab -nodisplay -r "addpath('./cafa2_eval/myscript');fmax_new('./cafa2_eval/matlab','CCO','./data/go-basic.obo','./data/pro_label/cafa3_fun_pro_cco.tsv','cafa3_train/tfpssm_13/nfold/cco/fold${fold}/cath_vote_pro_m0.txt','./cafa3_train/tfpssm_13/nfold/cco/fold${fold}/test_ID_list.txt','./cafa3_train/tfpssm_13/nfold/cco/fold${fold}/cath_vote_pro_m0_res.txt');quit;"
  # #enrich at pro
  # python python/gorelation/enrich.py -i cafa3_train/tfpssm_13/nfold/cco/fold${fold}/cath_vote_pro_m0.txt -r python/gorelation/cafa3_cco_rel.tsv -o cafa3_train/tfpssm_13/nfold/cco/fold${fold}/cath_vote_pro_m0_enrich.txt
  # matlab -nodisplay -r "addpath('./cafa2_eval/myscript');fmax_new('./cafa2_eval/matlab','CCO','./data/go-basic.obo','./data/pro_label/cafa3_fun_pro_cco.tsv','cafa3_train/tfpssm_13/nfold/cco/fold${fold}/cath_vote_pro_m0_enrich.txt','./cafa3_train/tfpssm_13/nfold/cco/fold${fold}/test_ID_list.txt','./cafa3_train/tfpssm_13/nfold/cco/fold${fold}/cath_vote_pro_m0_enrich_res.txt');quit;"

  #leafvote test
  #leaf
  python python/leafVote/leafVote.py -i cafa3_train/tfpssm_13/nfold/cco/fold${fold}/cco_knn.tsv -l data/labels/cafa3_function-C.tsv -s 0 -o cafa3_train/tfpssm_13/nfold/cco/fold${fold}/leaf_vote.txt
  matlab -nodisplay -r "addpath('./cafa2_eval/myscript');fmax_new('./cafa2_eval/matlab','CCO','./data/go-basic.obo','./data/pro_label/cafa3_fun_pro_cco.tsv','cafa3_train/tfpssm_13/nfold/cco/fold${fold}/leaf_vote.txt','./cafa3_train/tfpssm_13/nfold/cco/fold${fold}/test_ID_list.txt','./cafa3_train/tfpssm_13/nfold/cco/fold${fold}/leaf_vote_res.txt');quit;"
  #enrich at leaf
  python python/gorelation/enrich.py -i cafa3_train/tfpssm_13/nfold/cco/fold${fold}/leaf_vote.txt -r python/gorelation/cafa3_cco_rel.tsv -o cafa3_train/tfpssm_13/nfold/cco/fold${fold}/leaf_vote_enrich.txt
  matlab -nodisplay -r "addpath('./cafa2_eval/myscript');fmax_new('./cafa2_eval/matlab','CCO','./data/go-basic.obo','./data/pro_label/cafa3_fun_pro_cco.tsv','cafa3_train/tfpssm_13/nfold/cco/fold${fold}/leaf_vote_enrich.txt','./cafa3_train/tfpssm_13/nfold/cco/fold${fold}/test_ID_list.txt','./cafa3_train/tfpssm_13/nfold/cco/fold${fold}/leaf_vote_enrich_res.txt');quit;"

  #pro
  python python/leafVote/leafVote.py -i cafa3_train/tfpssm_13/nfold/cco/fold${fold}/cco_knn.tsv -l data/pro_label/cafa3_fun_pro_cco.tsv -s 0 -o cafa3_train/tfpssm_13/nfold/cco/fold${fold}/pro_vote.txt
  matlab -nodisplay -r "addpath('./cafa2_eval/myscript');fmax_new('./cafa2_eval/matlab','CCO','./data/go-basic.obo','./data/pro_label/cafa3_fun_pro_cco.tsv','cafa3_train/tfpssm_13/nfold/cco/fold${fold}/pro_vote.txt','./cafa3_train/tfpssm_13/nfold/cco/fold${fold}/test_ID_list.txt','./cafa3_train/tfpssm_13/nfold/cco/fold${fold}/pro_vote_res.txt');quit;"
  #enrich at pro
  python python/gorelation/enrich.py -i cafa3_train/tfpssm_13/nfold/cco/fold${fold}/pro_vote.txt -r python/gorelation/cafa3_cco_rel.tsv -o cafa3_train/tfpssm_13/nfold/cco/fold${fold}/pro_vote_enrich.txt
  matlab -nodisplay -r "addpath('./cafa2_eval/myscript');fmax_new('./cafa2_eval/matlab','CCO','./data/go-basic.obo','./data/pro_label/cafa3_fun_pro_cco.tsv','cafa3_train/tfpssm_13/nfold/cco/fold${fold}/pro_vote_enrich.txt','./cafa3_train/tfpssm_13/nfold/cco/fold${fold}/test_ID_list.txt','./cafa3_train/tfpssm_13/nfold/cco/fold${fold}/pro_vote_enrich_res.txt');quit;"

done
