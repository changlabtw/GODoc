#!/bin/bash

#for i in $(seq 1 20)
for i in 13
do
  #BPO
  python python/gorelation/enrich.py -i tfpssm_exp/tfpssm_${i}/bpo_type1/pro_score.txt -r python/gorelation/cafa3_bpo_rel.tsv -o tfpssm_exp/tfpssm_${i}/bpo_type1/enrich_score.txt
  matlab -nodisplay -r "addpath('./cafa2_eval/myscript');fmax('./cafa2_eval/matlab','BPO','./cafa2_eval/ontology/','./cafa2_eval/benchmark/groundtruth/propagated_BPO.txt','tfpssm_exp/tfpssm_${i}/bpo_type1/enrich_score.txt','./cafa2_eval/benchmark/lists/bpo_all_type1.txt','tfpssm_exp/tfpssm_${i}/bpo_type1/enrich_res.txt');quit;"
  python python/gorelation/enrich.py -i tfpssm_exp/tfpssm_${i}/bpo_type2/pro_score.txt -r python/gorelation/cafa3_bpo_rel.tsv -o tfpssm_exp/tfpssm_${i}/bpo_type2/enrich_score.txt
  matlab -nodisplay -r "addpath('./cafa2_eval/myscript');fmax('./cafa2_eval/matlab','BPO','./cafa2_eval/ontology/','./cafa2_eval/benchmark/groundtruth/propagated_BPO.txt','tfpssm_exp/tfpssm_${i}/bpo_type2/enrich_score.txt','./cafa2_eval/benchmark/lists/bpo_all_type2.txt','tfpssm_exp/tfpssm_${i}/bpo_type2/enrich_res.txt');quit;"

  #CCO
  python python/gorelation/enrich.py -i tfpssm_exp/tfpssm_${i}/cco_type1/pro_score.txt -r python/gorelation/cafa3_cco_rel.tsv -o tfpssm_exp/tfpssm_${i}/cco_type1/enrich_score.txt
  matlab -nodisplay -r "addpath('./cafa2_eval/myscript');fmax('./cafa2_eval/matlab','CCO','./cafa2_eval/ontology/','./cafa2_eval/benchmark/groundtruth/propagated_CCO.txt','tfpssm_exp/tfpssm_${i}/cco_type1/enrich_score.txt','./cafa2_eval/benchmark/lists/cco_all_type1.txt','tfpssm_exp/tfpssm_${i}/cco_type1/enrich_res.txt');quit;"
  python python/gorelation/enrich.py -i tfpssm_exp/tfpssm_${i}/cco_type2/pro_score.txt -r python/gorelation/cafa3_cco_rel.tsv -o tfpssm_exp/tfpssm_${i}/cco_type2/enrich_score.txt
  matlab -nodisplay -r "addpath('./cafa2_eval/myscript');fmax('./cafa2_eval/matlab','CCO','./cafa2_eval/ontology/','./cafa2_eval/benchmark/groundtruth/propagated_CCO.txt','tfpssm_exp/tfpssm_${i}/cco_type2/enrich_score.txt','./cafa2_eval/benchmark/lists/cco_all_type2.txt','tfpssm_exp/tfpssm_${i}/cco_type2/enrich_res.txt');quit;"

  #MFO
  python python/gorelation/enrich.py -i tfpssm_exp/tfpssm_${i}/mfo_type1/pro_score.txt -r python/gorelation/cafa3_mfo_rel.tsv -o tfpssm_exp/tfpssm_${i}/mfo_type1/enrich_score.txt
  matlab -nodisplay -r "addpath('./cafa2_eval/myscript');fmax('./cafa2_eval/matlab','MFO','./cafa2_eval/ontology/','./cafa2_eval/benchmark/groundtruth/propagated_MFO.txt','tfpssm_exp/tfpssm_${i}/mfo_type1/enrich_score.txt','./cafa2_eval/benchmark/lists/mfo_all_type1.txt','tfpssm_exp/tfpssm_${i}/mfo_type1/enrich_res.txt');quit;"
  python python/gorelation/enrich.py -i tfpssm_exp/tfpssm_${i}/mfo_type2/pro_score.txt -r python/gorelation/cafa3_mfo_rel.tsv -o tfpssm_exp/tfpssm_${i}/mfo_type2/enrich_score.txt
  matlab -nodisplay -r "addpath('./cafa2_eval/myscript');fmax('./cafa2_eval/matlab','MFO','./cafa2_eval/ontology/','./cafa2_eval/benchmark/groundtruth/propagated_MFO.txt','tfpssm_exp/tfpssm_${i}/mfo_type2/enrich_score.txt','./cafa2_eval/benchmark/lists/mfo_all_type2.txt','tfpssm_exp/tfpssm_${i}/mfo_type2/enrich_res.txt');quit;"
done
