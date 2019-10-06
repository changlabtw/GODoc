#!/bin/bash

touch cafa3_train/oneNN_res.csv

for i in $(seq 1 40)
do
  for t in bpo cco mfo
  do
    for f in $(seq 0 4)
    do
      #oneNN
      echo -n ${t},${i},${f}, | tail -n 1 -q - cafa3_train/tfpssm_${i}/nfold/${t}/fold${f}/pro_res.txt >> cafa3_train/oneNN_res.csv
    done
  done
done
