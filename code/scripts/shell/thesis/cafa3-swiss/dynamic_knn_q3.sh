#!/bin/bash
# PCA experiment
# PCA vector files must be [nfold_root]/pca/[explain_ratio]
if [ "$#" -ne 5 ]; then
    echo "Illegal number of parameters, must eqal 5."
    echo "Usage: ./fixed_knn.sh [nfold folder root] [data folder root] [PCA folder root] [PCA explain ratio] [type]"
    exit
fi
echo nfold folder root: ${1}
echo data folder root: ${2}
echo PCA folder root: ${3}
echo PCA explain ratio: ${4}
echo Type: ${5}

nfold_root=${1}
data_root=${2}
pca_root=${3}
explain_ratio=${4}
target_type=${5}

for t in ${target_type}
do
  for fold in 0 1 2 3 4
  do
    pca_path=${nfold_root}/${t}/fold$fold/${pca_root}/${explain_ratio}/w/nr
    python python/knn/dynamic_knn_exp.py -b ${nfold_root}/$t/fold$fold/${data_root}/train_1nn_res.tsv \
                             -train ${pca_path}/train_tfpssm_pca.csv \
                             -test ${pca_path}/test_tfpssm_pca.csv \
                             -o ${nfold_root}/$t/fold$fold/${data_root}/test_q3_res.tsv
  done
done
