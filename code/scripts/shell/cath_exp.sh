#!/bin/bash
for thres in 25 50 75
do
  python python/knn/dynamic_knn.py -b tfpssm_exp/tfpssm_13/pca_result.csv -train swiss/cco/train_vec.csv -test tfpssm_exp/tfpssm_13/target.csv -t ${thres}% -o swiss/cco/cath/cco_${thres}_knn.tsv
  for sel in sf funfam model
  do
    for method in 0 1 2
    do
      python python/cath/knn_filter.py -i swiss/cco/cath/cco_${thres}_knn.tsv -train cath/all_map.tsv -target cath/cafa2_target_map.tsv -m ${method} -sel ${sel} -o swiss/cco/cath/filtered_knn_${thres}_${method}_${sel}.tsv
      for score in 0 1 2 3
      do
        python python/leafVote/leafVote.py -i swiss/cco/cath/filtered_knn_${thres}_${method}_${sel}.tsv -l data/labels/all_function-C.tsv -s ${score} -o swiss/cco/cath/leafscore_${thres}_${method}_${sel}_${score}.txt
        python python/propagate/propagate.py -i swiss/cco/cath/leafscore_${thres}_${method}_${sel}_${score}.txt -db data/go-basic.obo -o swiss/cco/cath/proscore_${thres}_${method}_${sel}_${score}.txt
        matlab -nodisplay -r "addpath('./cafa2_eval/myscript');fmax('./cafa2_eval/matlab','CCO','./cafa2_eval/ontology/','./cafa2_eval/benchmark/groundtruth/propagated_CCO.txt','swiss/cco/cath/proscore_${thres}_${method}_${sel}_${score}.txt','./cafa2_eval/benchmark/lists/cco_all_type1.txt','swiss/cco/cath/proscore_${thres}_${method}_${sel}_${score}_res.txt');quit;"
      done
    done
  done
done
