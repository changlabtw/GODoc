#!/bin/bash
# Dynamic KNN Experiment
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
    for q in q1 q2 q3
    do
      mkdir ${nfold_root}/$t/fold$fold/${data_root}/${q}
      output_path=${nfold_root}/$t/fold$fold/${data_root}/${q}
      for lt in pro leaf
      do
        mkdir ${output_path}/${lt}
        for method in 0 2 6
        do
          cur_path=${output_path}/${lt}/${method}
          mkdir ${cur_path}
          python python/leafVote/leafVote.py -i ${nfold_root}/$t/fold$fold/${data_root}/test_${q}_res.tsv \
                                             -l ${nfold_root}/$t/fold$fold/train_${lt}.txt \
                                             -s ${method} -o ${cur_path}/vote_score.tsv
          if [ ! -f ${cur_path}/fmax.txt ]
          then
            # seq_eval(matlab_path, cat, ont_db_path, oa_file, pred_file, benchmark_file, output_folder)
            matlab -nodisplay -r "addpath('./cafa2_eval/myscript');\
            seq_eval('./cafa2_eval/matlab','$t','./data/go_20130615-termdb.obo',\
            '${nfold_root}/$t/fold$fold/test_pro.txt',\
            '${cur_path}/vote_score.tsv',\
            '${nfold_root}/$t/fold$fold/test_ID.txt',\
            '${cur_path}');quit;"
          fi
        done
      done
    done
  done
done
