#!/bin/bash
res=thesis/data/cafa2_train/res.csv
if [ -f "$res" ]
then
  echo '$res already exists, remove it.'
  rm ${res}
else
  touch ${res}
fi
for t in bpo cco mfo
do
  for fold in 0 1 2 3 4
  do
    cur_fold=thesis/data/cafa2_train/nfold/$t/fold$fold
    #naive
    echo -n ${t},${fold},naive_leaf, | tail -n 1 -q - $cur_fold/naive_leaf/fmax.txt >> $res
    echo -n ${t},${fold},naive_pro, | tail -n 1 -q - $cur_fold/naive_pro/fmax.txt >> $res
    #blast
    echo -n ${t},${fold},blast, | tail -n 1 -q - $cur_fold/blast/fmax.txt >> $res
    #tfpssm_1nn
    echo -n ${t},${fold},tfpssm_1nn, | tail -n 1 -q - $cur_fold/tfpssm_1nn/fmax.txt >> $res
    #ctd_1nn
    echo -n ${t},${fold},ctd_1nn, | tail -n 1 -q - $cur_fold/ctd_1nn/fmax.txt >> $res
    #purectd_1nn
    echo -n ${t},${fold},purectd_1nn, | tail -n 1 -q - $cur_fold/ctd_pure_1nn/fmax.txt >> $res
    #ctd+tfpssm_1nn
    echo -n ${t},${fold},ctd+tfpssm_1nn, | tail -n 1 -q - $cur_fold/ctd+tfpssm_1nn/fmax.txt >> $res
    # tfpssm_cathvote, tfpssm_vote
    for p in 25 50 75
    do
      for lt in pro leaf
      do
        echo -n ${t},${fold},tfpssm_vote_${p}_${lt}, | tail -n 1 -q - $cur_fold/${lt}_vote/${p}/fmax.txt >> $res
        echo -n ${t},${fold},tfpssm_cathvote$_${p}_${lt}, | tail -n 1 -q - $cur_fold/${lt}_cathvote/${p}/fmax.txt >> $res
      done
    done
  done
done
