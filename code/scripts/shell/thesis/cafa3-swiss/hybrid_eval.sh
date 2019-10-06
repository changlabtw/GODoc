#!/bin/bash
# Hybrid KNN Experiment
if [ "$#" -ne 3 ]; then
    echo "Illegal number of parameters, must eqal 3."
    echo "Usage: ./hybrid_knn.sh [nfold folder root] [data folder root] [type]"
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
    output_path=${nfold_root}/$t/fold$fold/${data_root}/hybrid
    for q in q2
    do
      for k in 1 2 3 4 5 6 7 8 9 10
      do
        hybrid_path=${output_path}/${q}_${k}
        for lt in pro
        do
          for method in 0 2 6
          do
            for based in dynamic
            do
              if [ ! -f ${cur_path}/fmax.txt ]
              then
                while [ $(jobs | wc -l) -ge 12 ] ; do sleep 1 ; done
                # seq_eval(matlab_path, cat, ont_db_path, oa_file, pred_file, benchmark_file, output_folder)
                matlab -nodisplay -r "addpath('./cafa2_eval/myscript');\
                seq_eval('./cafa2_eval/matlab','$t','./data/go_20160601-termdb.obo',\
                '${nfold_root}/$t/fold$fold/test_pro.txt',\
                '${hybrid_path}/${lt}/${method}/${based}/vote_score.tsv',\
                '${nfold_root}/$t/fold$fold/test_ID.txt',\
                '${hybrid_path}/${lt}/${method}/${based}');quit;" &
              fi
            done
          done
        done
      done
    done
  done
done
