#!/bin/bash
# PCA experiment
# PCA vector files must be [nfold_root]/pca/[explain_ratio]
if [ "$#" -ne 3 ]; then
    echo "Illegal number of parameters, must eqal 3."
    echo "Usage: ./fixed_knn.sh [nfold folder root] [data folder root] [type]"
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
    for k in 1 2 3 4 5 6 7 8 9 10
    do
      mkdir ${nfold_root}/$t/fold$fold/${data_root}/hard_q2
      output_path=${nfold_root}/$t/fold$fold/${data_root}/hard_q2/${k}
      mkdir ${output_path}
      for lt in pro
      do
        mkdir ${output_path}/${lt}
        for method in 0 2 6
        do
          cur_path=${output_path}/${lt}/${method}
          if [ ! -f ${cur_path}/partial_fmax.txt ]
          then
            while [ $(jobs | wc -l) -ge 12 ] ; do sleep 1 ; done
            # seq_eval(matlab_path, cat, ont_db_path, oa_file, pred_file, benchmark_file, output_folder)
            matlab -nodisplay -r "addpath('./cafa2_eval/myscript');\
            seq_eval('./cafa2_eval/matlab','$t','./data/go_20160601-termdb.obo',\
            '${nfold_root}/$t/fold$fold/test_pro.txt',\
            '${nfold_root}/$t/fold$fold/${data_root}/${k}/${lt}/${method}/vote_score.tsv',\
            '${nfold_root}/$t/fold$fold/knn_exp/test_q2_hard_ID.txt',\
            '${cur_path}', '2');quit;" &
          fi
        done
      done
    done
  done
done
