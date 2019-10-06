#!/bin/bash
# CATH Dynamic KNN Experiment
# PCA vector files must be [nfold_root]/pca/[explain_ratio]
if [ "$#" -ne 3 ]; then
    echo "Illegal number of parameters, must eqal 3."
    echo "Usage: ./cath_dynamic_knn.sh [folder root] [data folder root] [type]"
    exit
fi
echo nfold folder root: ${1}
echo data folder root: ${2}
echo Type: ${3}

folder_root=${1}
nfold_root=${1}/nfold
data_root=${2}
target_type=${3}

for t in ${target_type}
do
  for fold in 0 1 2 3 4
  do
    for q in q1 q2 q3
    do
      output_path=${nfold_root}/$t/fold$fold/${data_root}/cath
      mkdir ${output_path}
      python python/cath/ff_filter.py -i ${nfold_root}/$t/fold$fold/${data_root}/test_${q}_res.tsv \
                                      -test_m ${folder_root}/cafa3_train_ff_ind.pkl \
                                      -train_m ${folder_root}/cafa3_train_ff_ind.pkl \
                                      -o ${output_path}/cath_test_${q}_res.tsv
      for lt in pro
      do
        for method in cath
        do
          cur_path=${output_path}/${q}
          mkdir ${cur_path}
          python python/cath/cath_vote_multi.py -i ${output_path}/cath_test_${q}_res.tsv \
                                                -l ${nfold_root}/$t/fold$fold/train_${lt}.txt \
                                                -m 2 -o ${cur_path}/vote_score.tsv
        done
      done
    done
  done
done
