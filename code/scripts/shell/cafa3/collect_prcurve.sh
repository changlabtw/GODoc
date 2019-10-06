#!/bin/bash
root_path=thesis/data/cafa3_train
for t in bpo cco mfo
do
  mkdir ${root_path}/nfold/$t/prcurve
  for methods in naive_leaf blast tfpssm_1nn pro_vote/75 pro_cathvote/75
  do
    cur_files=""
    for fold in 0 1 2 3 4
    do
      cur_fold=${root_path}/nfold/$t/fold$fold
      cur_files="${cur_files}${cur_fold}/${methods}/prcurve.csv "
    done
    if [ "$methods" == "pro_vote/75" ]
    then
      python python/plot/prcurve_collect.py -v ${cur_files} -o ${root_path}/nfold/$t/prcurve/pro_vote.csv
    elif [ "$methods" == "pro_cathvote/75" ]
    then
      python python/plot/prcurve_collect.py -v ${cur_files} -o ${root_path}/nfold/$t/prcurve/pro_cathvote.csv
    else
      python python/plot/prcurve_collect.py -v ${cur_files} -o ${root_path}/nfold/$t/prcurve/${methods}.csv
    fi
  done
done
