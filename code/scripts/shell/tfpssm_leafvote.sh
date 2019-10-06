#!/bin/bash

# for i in $(seq 1 20)
for i in 13
do
  mkdir tfpssm_exp/tfpssm_${i}/leafvote

  for threshold in 25 50 75
  do
    python python/knn/dynamic_knn.py -b tfpssm_exp/tfpssm_${i}/pca_result.csv -train tfpssm_exp/tfpssm_${i}/bpo_pca_result.csv -test tfpssm_exp/tfpssm_${i}/target.csv -t ${threshold}% -o tfpssm_exp/tfpssm_${i}/leafvote/bpo_${threshold}_knn.tsv
    python python/knn/dynamic_knn.py -b tfpssm_exp/tfpssm_${i}/pca_result.csv -train tfpssm_exp/tfpssm_${i}/cco_pca_result.csv -test tfpssm_exp/tfpssm_${i}/target.csv -t ${threshold}% -o tfpssm_exp/tfpssm_${i}/leafvote/cco_${threshold}_knn.tsv
    python python/knn/dynamic_knn.py -b tfpssm_exp/tfpssm_${i}/pca_result.csv -train tfpssm_exp/tfpssm_${i}/mfo_pca_result.csv -test tfpssm_exp/tfpssm_${i}/target.csv -t ${threshold}% -o tfpssm_exp/tfpssm_${i}/leafvote/mfo_${threshold}_knn.tsv
    for formula in 0 1 2
    do
      #BPO
      python python/leafVote/leafVote.py -i tfpssm_exp/tfpssm_${i}/leafvote/bpo_${threshold}_knn.tsv -l data/labels/all_function-P.tsv -s ${formula} -o tfpssm_exp/tfpssm_${i}/leafvote/bpo_${threshold}_${formula}_leafscore.txt
      python python/propagate/propagate.py -i tfpssm_exp/tfpssm_${i}/leafvote/bpo_${threshold}_${formula}_leafscore.txt -o tfpssm_exp/tfpssm_${i}/leafvote/bpo_${threshold}_${formula}_proscore.txt -db data/go-basic.obo
      matlab -nodisplay -r "addpath('./cafa2_eval/myscript');fmax('./cafa2_eval/matlab','BPO','./cafa2_eval/ontology/','./cafa2_eval/benchmark/groundtruth/propagated_BPO.txt','tfpssm_exp/tfpssm_${i}/leafvote/bpo_${threshold}_${formula}_proscore.txt','./cafa2_eval/benchmark/lists/bpo_all_type1.txt','tfpssm_exp/tfpssm_${i}/leafvote/bpo${threshold}_${formula}_prores_type1.txt');quit;"
      matlab -nodisplay -r "addpath('./cafa2_eval/myscript');fmax('./cafa2_eval/matlab','BPO','./cafa2_eval/ontology/','./cafa2_eval/benchmark/groundtruth/propagated_BPO.txt','tfpssm_exp/tfpssm_${i}/leafvote/bpo_${threshold}_${formula}_proscore.txt','./cafa2_eval/benchmark/lists/bpo_all_type2.txt','tfpssm_exp/tfpssm_${i}/leafvote/bpo${threshold}_${formula}_prores_type2.txt');quit;"

      #CCO
      python python/leafVote/leafVote.py -i tfpssm_exp/tfpssm_${i}/leafvote/cco_${threshold}_knn.tsv -l data/labels/all_function-C.tsv -s ${formula} -o tfpssm_exp/tfpssm_${i}/leafvote/cco_${threshold}_${formula}_leafscore.txt
      python python/propagate/propagate.py -i tfpssm_exp/tfpssm_${i}/leafvote/cco_${threshold}_${formula}_leafscore.txt -o tfpssm_exp/tfpssm_${i}/leafvote/cco_${threshold}_${formula}_proscore.txt -db data/go-basic.obo
      matlab -nodisplay -r "addpath('./cafa2_eval/myscript');fmax('./cafa2_eval/matlab','CCO','./cafa2_eval/ontology/','./cafa2_eval/benchmark/groundtruth/propagated_CCO.txt','tfpssm_exp/tfpssm_${i}/leafvote/cco_${threshold}_${formula}_proscore.txt','./cafa2_eval/benchmark/lists/cco_all_type1.txt','tfpssm_exp/tfpssm_${i}/leafvote/cco${threshold}_${formula}_prores_type1.txt');quit;"
      matlab -nodisplay -r "addpath('./cafa2_eval/myscript');fmax('./cafa2_eval/matlab','CCO','./cafa2_eval/ontology/','./cafa2_eval/benchmark/groundtruth/propagated_CCO.txt','tfpssm_exp/tfpssm_${i}/leafvote/cco_${threshold}_${formula}_proscore.txt','./cafa2_eval/benchmark/lists/cco_all_type2.txt','tfpssm_exp/tfpssm_${i}/leafvote/cco${threshold}_${formula}_prores_type2.txt');quit;"

      #MFO
      python python/leafVote/leafVote.py -i tfpssm_exp/tfpssm_${i}/leafvote/mfo_${threshold}_knn.tsv -l data/labels/all_function-F.tsv -s ${formula} -o tfpssm_exp/tfpssm_${i}/leafvote/mfo_${threshold}_${formula}_leafscore.txt
      python python/propagate/propagate.py -i tfpssm_exp/tfpssm_${i}/leafvote/mfo_${threshold}_${formula}_leafscore.txt -o tfpssm_exp/tfpssm_${i}/leafvote/mfo_${threshold}_${formula}_proscore.txt -db data/go-basic.obo
      matlab -nodisplay -r "addpath('./cafa2_eval/myscript');fmax('./cafa2_eval/matlab','MFO','./cafa2_eval/ontology/','./cafa2_eval/benchmark/groundtruth/propagated_MFO.txt','tfpssm_exp/tfpssm_${i}/leafvote/mfo_${threshold}_${formula}_proscore.txt','./cafa2_eval/benchmark/lists/mfo_all_type1.txt','tfpssm_exp/tfpssm_${i}/leafvote/mfo${threshold}_${formula}_prores_type1.txt');quit;"
      matlab -nodisplay -r "addpath('./cafa2_eval/myscript');fmax('./cafa2_eval/matlab','MFO','./cafa2_eval/ontology/','./cafa2_eval/benchmark/groundtruth/propagated_MFO.txt','tfpssm_exp/tfpssm_${i}/leafvote/mfo_${threshold}_${formula}_proscore.txt','./cafa2_eval/benchmark/lists/mfo_all_type2.txt','tfpssm_exp/tfpssm_${i}/leafvote/mfo${threshold}_${formula}_prores_type2.txt');quit;"
    done
  done
done
