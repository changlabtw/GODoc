#!/bin/bash
res=thesis/data/cafa2_target/res.csv
if [ -f "$res" ]
then
  echo '$res already exists, remove it.'
  rm ${res}
else
  touch ${res}
fi
for t in bpo cco mfo
do
  for bt in 1 2
  do
    cur_folder=thesis/data/cafa2_target
    #naive
    echo -n ${t}_type${bt},naive, | tail -n 1 -q - $cur_folder/naive/${t}_type${bt}/fmax.txt >> $res
    #blast
    echo -n ${t}_type${bt},blast, | tail -n 1 -q - $cur_folder/blast/${t}_type${bt}/fmax.txt >> $res
    #tfpssm_1nn
    echo -n ${t}_type${bt},tfpssm_1nn, | tail -n 1 -q - $cur_folder/tfpssm_1nn/${t}_type${bt}/fmax.txt >> $res
    #ctd_1nn
    echo -n ${t}_type${bt},ctd_1nn, | tail -n 1 -q - $cur_folder/ctd_1nn/${t}_type${bt}/fmax.txt >> $res
    #purectd_1nn
    echo -n ${t}_type${bt},purectd_1nn, | tail -n 1 -q - $cur_folder/ctd_pure_1nn/${t}_type${bt}/fmax.txt >> $res
    #ctd+tfpssm_1nn
    echo -n ${t}_type${bt},ctd+tfpssm_1nn, | tail -n 1 -q - $cur_folder/ctd+tfpssm_1nn/${t}_type${bt}/fmax.txt >> $res
    # tfpssm_cathvote, tfpssm_vote
    for lt in pro leaf
    do
      for p in 25 50 75
      do
        echo -n ${t}_type${bt},tfpssm_vote_${p}_${lt}, | tail -n 1 -q - $cur_folder/${lt}_vote/${t}_type${bt}/${p}/fmax.txt >> $res
        echo -n ${t}_type${bt},tfpssm_cathvote$_${p}_${lt}, | tail -n 1 -q - $cur_folder/${lt}_cathvote/${t}_type${bt}/${p}/fmax.txt >> $res
      done
    done
  done
done
