#!/bin/bash
# Split Dynamic KNN Q3 result to Q1 and Q2
# PCA vector files must be [nfold_root]/pca/[explain_ratio]
if [ "$#" -ne 3 ]; then
    echo "Illegal number of parameters, must eqal 5."
    echo "Usage: ./dynamic_knn_split.sh [nfold folder root] [data folder root] [type]"
    exit
fi
echo nfold folder root: ${1}
echo data folder root: ${2}
echo Type: ${3}

nfold_root=${1}
data_root=${2}
target_type=${3}

for t in ${target_type}
do
  for fold in 0 1 2 3 4
  do
    for q in 1 2
    do
      python python/knn/dynamic_knn_split.py -b ${nfold_root}/$t/fold$fold/${data_root}/train_1nn_res.tsv \
                               -i ${nfold_root}/$t/fold$fold/${data_root}/test_q3_res.tsv \
                               -q ${q} -o ${nfold_root}/$t/fold$fold/${data_root}/test_q${q}_res.tsv
    done
  done
done
