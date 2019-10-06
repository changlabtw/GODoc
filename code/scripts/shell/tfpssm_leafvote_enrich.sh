#!/bin/bash

for i in $(seq 1 20)
do
  for threshold in 25
  do
    for formula in 3
    do
      #BPO
      python python/gorelation/enrich.py -i tfpssm_exp/tfpssm_${i}/leafvote/bpo_${threshold}_${formula}_proscore.txt -r python/gorelation/cafa3_bpo_rel.tsv -o tfpssm_exp/tfpssm_${i}/leafvote/bpo_${threshold}_${formula}_proscore_enrich.txt
      matlab -nodisplay -r "addpath('./cafa2_eval/myscript');fmax('./cafa2_eval/matlab','BPO','./cafa2_eval/ontology/','./cafa2_eval/benchmark/groundtruth/propagated_BPO.txt','tfpssm_exp/tfpssm_${i}/leafvote/bpo_${threshold}_${formula}_proscore_enrich.txt','./cafa2_eval/benchmark/lists/bpo_all_type1.txt','tfpssm_exp/tfpssm_${i}/leafvote/bpo_${threshold}_${formula}_proscore_enrich_type1.txt');quit;"
      matlab -nodisplay -r "addpath('./cafa2_eval/myscript');fmax('./cafa2_eval/matlab','BPO','./cafa2_eval/ontology/','./cafa2_eval/benchmark/groundtruth/propagated_BPO.txt','tfpssm_exp/tfpssm_${i}/leafvote/bpo_${threshold}_${formula}_proscore_enrich.txt','./cafa2_eval/benchmark/lists/bpo_all_type2.txt','tfpssm_exp/tfpssm_${i}/leafvote/bpo_${threshold}_${formula}_proscore_enrich_type2.txt');quit;"

      #CCO
      python python/gorelation/enrich.py -i tfpssm_exp/tfpssm_${i}/leafvote/cco_${threshold}_${formula}_proscore.txt -r python/gorelation/cafa3_cco_rel.tsv -o tfpssm_exp/tfpssm_${i}/leafvote/cco_${threshold}_${formula}_proscore_enrich.txt
      matlab -nodisplay -r "addpath('./cafa2_eval/myscript');fmax('./cafa2_eval/matlab','CCO','./cafa2_eval/ontology/','./cafa2_eval/benchmark/groundtruth/propagated_CCO.txt','tfpssm_exp/tfpssm_${i}/leafvote/cco_${threshold}_${formula}_proscore_enrich.txt','./cafa2_eval/benchmark/lists/cco_all_type1.txt','tfpssm_exp/tfpssm_${i}/leafvote/cco_${threshold}_${formula}_proscore_enrich_type1.txt');quit;"
      matlab -nodisplay -r "addpath('./cafa2_eval/myscript');fmax('./cafa2_eval/matlab','CCO','./cafa2_eval/ontology/','./cafa2_eval/benchmark/groundtruth/propagated_CCO.txt','tfpssm_exp/tfpssm_${i}/leafvote/cco_${threshold}_${formula}_proscore_enrich.txt','./cafa2_eval/benchmark/lists/cco_all_type2.txt','tfpssm_exp/tfpssm_${i}/leafvote/cco_${threshold}_${formula}_proscore_enrich_type2.txt');quit;"

      #MFO
      python python/gorelation/enrich.py -i tfpssm_exp/tfpssm_${i}/leafvote/mfo_${threshold}_${formula}_proscore.txt -r python/gorelation/cafa3_mfo_rel.tsv -o tfpssm_exp/tfpssm_${i}/leafvote/mfo_${threshold}_${formula}_proscore_enrich.txt
      matlab -nodisplay -r "addpath('./cafa2_eval/myscript');fmax('./cafa2_eval/matlab','MFO','./cafa2_eval/ontology/','./cafa2_eval/benchmark/groundtruth/propagated_MFO.txt','tfpssm_exp/tfpssm_${i}/leafvote/mfo_${threshold}_${formula}_proscore_enrich.txt','./cafa2_eval/benchmark/lists/mfo_all_type1.txt','tfpssm_exp/tfpssm_${i}/leafvote/mfo_${threshold}_${formula}_proscore_enrich_type1.txt');quit;"
      matlab -nodisplay -r "addpath('./cafa2_eval/myscript');fmax('./cafa2_eval/matlab','MFO','./cafa2_eval/ontology/','./cafa2_eval/benchmark/groundtruth/propagated_MFO.txt','tfpssm_exp/tfpssm_${i}/leafvote/mfo_${threshold}_${formula}_proscore_enrich.txt','./cafa2_eval/benchmark/lists/mfo_all_type2.txt','tfpssm_exp/tfpssm_${i}/leafvote/mfo_${threshold}_${formula}_proscore_enrich_type2.txt');quit;"

    done
  done
done
