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
      for lt in pro
      do
        for method in cath
        do
          cur_path=${output_path}/${q}
          if [ ! -f ${cur_path}/partial_fmax.txt ]
          then
            while [ $(jobs | wc -l) -ge 12 ] ; do sleep 1 ; done
            # seq_eval(matlab_path, cat, ont_db_path, oa_file, pred_file, benchmark_file, output_folder)
            matlab -nodisplay -r "addpath('./cafa2_eval/myscript');\
            seq_eval('./cafa2_eval/matlab','$t','./data/go_20160601-termdb.obo',\
            '${nfold_root}/$t/fold$fold/test_pro.txt',\
            '${cur_path}/vote_score.tsv',\
            '${nfold_root}/$t/fold$fold/test_ID.txt',\
            '${cur_path}','2');quit;"
          fi
        done
      done
    done
  done
done
