#!/bin/bash
# Add FunFam intersection amout to 10nn results
# PCA vector files must be [nfold_root]/pca/[explain_ratio]
if [ "$#" -ne 3 ]; then
    echo "Illegal number of parameters, must eqal 3."
    echo "Usage: ./cath_10nn.sh [folder root] [data folder root] [type]"
    exit
fi
echo folder root: ${1}
echo data folder root: ${2}
echo Type: ${3}

folder_root=${1}
data_root=${2}
target_type=${3}

for t in ${target_type}
do
  for fold in 0 1 2 3 4
  do
    python python/cath/ff_filter.py -i ${folder_root}/nfold/$t/fold$fold/${data_root}/10nn_res.tsv \
                                    -test_m ${folder_root}/cafa2_train_ff_ind.pkl \
                                    -train_m ${folder_root}/cafa2_train_ff_ind.pkl \
                                    -o ${folder_root}/nfold/$t/fold$fold/${data_root}/cath_10nn_res.tsv
  done
done
