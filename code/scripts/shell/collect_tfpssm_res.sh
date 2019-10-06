#!/bin/bash

#touch tfpssm_exp/oneNN_res.csv
#touch tfpssm_exp/leafvote_res.csv
#touch tfpssm_exp/leafvote_threshold_res.csv
# touch tfpssm_exp/oneNN_enrich_res.csv

for i in $(seq 1 20)
do
  for t in bpo cco mfo
  do
    #oneNN
    # echo -n ${t}_type1,${i}, | tail -n 1 -q - tfpssm_exp/tfpssm_${i}/${t}_type1/pro_res.txt >> tfpssm_exp/oneNN_res.csv
    # echo -n ${t}_type2,${i}, | tail -n 1 -q - tfpssm_exp/tfpssm_${i}/${t}_type2/pro_res.txt >> tfpssm_exp/oneNN_res.csv

    #oneNN_enrich
    # echo -n ${t}_type1,${i}, | tail -n 1 -q - tfpssm_exp/tfpssm_${i}/${t}_type1/enrich_res.txt >> tfpssm_exp/oneNN_enrich_res.csv
    # echo -n ${t}_type2,${i}, | tail -n 1 -q - tfpssm_exp/tfpssm_${i}/${t}_type2/enrich_res.txt >> tfpssm_exp/oneNN_enrich_res.csv

    # leafVote
    for threshold in 25 50 75
    do
      for formula in 3
      do
        # echo -n ${t}_type1,${i},${threshold},${formula}, | tail -n 1 -q - tfpssm_exp/tfpssm_${i}/leafvote_threshold/${t}${threshold}_${formula}_prores_type1.txt >> tfpssm_exp/leafvote_threshold_res.csv
        # echo -n ${t}_type2,${i},${threshold},${formula}, | tail -n 1 -q - tfpssm_exp/tfpssm_${i}/leafvote_threshold/${t}${threshold}_${formula}_prores_type2.txt >> tfpssm_exp/leafvote_threshold_res.csv
        echo -n ${t}_type1,${i},${threshold},${formula}, | tail -n 1 -q - tfpssm_exp/tfpssm_${i}/leafvote/${t}${threshold}_${formula}_prores_type1.txt >> tfpssm_exp/leafvote_res.csv
        echo -n ${t}_type2,${i},${threshold},${formula}, | tail -n 1 -q - tfpssm_exp/tfpssm_${i}/leafvote/${t}${threshold}_${formula}_prores_type2.txt >> tfpssm_exp/leafvote_res.csv
      done
    done
  done
done
