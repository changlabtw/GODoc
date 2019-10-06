#!/bin/bash

touch cafa3_train/oneNN_pruning_res.csv

for i in 3
do
  for t in cco mfo bpo
  do
    for f in $(seq 0 4)
    do
      for thres in $(seq 0.05 0.01 0.3)
      do
        #oneNN_pruning
        echo -n ${t},${i},${f},${thres}, | tail -n 1 -q - cafa3_train/tfpssm_${i}/nfold/${t}/fold${f}/pruning_${thres}_res.txt >> cafa3_train/oneNN_pruning_res.csv
      done
    done
  done
done
