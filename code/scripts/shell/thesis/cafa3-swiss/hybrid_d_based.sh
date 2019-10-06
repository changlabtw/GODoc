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
    mkdir ${output_path}
    for q in q2
    do
      for k in 1 2 3 4 5 6 7 8 9 10
      do
        hybrid_path=${output_path}/${q}_${k}
        mkdir ${hybrid_path}
        for lt in pro
        do
          mkdir ${hybrid_path}/${lt}
          for method in 0 2 6
          do
            mkdir ${hybrid_path}/${lt}/${method}
            for based in dynamic
            do
              mkdir ${hybrid_path}/${lt}/${method}/${based}
              python python/cath/cath_knn_merge.py -fs ${nfold_root}/$t/fold$fold/${data_root}/${k}/${lt}/${method}/vote_score.tsv \
                                                    -fk ${nfold_root}/$t/fold$fold/${data_root}/10nn_res.tsv \
                                                    -cs ${nfold_root}/$t/fold$fold/${data_root}/${q}/${lt}/${method}/vote_score.tsv \
                                                    -ck ${nfold_root}/$t/fold$fold/${data_root}/test_${q}_res.tsv \
                                                    -o ${hybrid_path}/${lt}/${method}/${based}/vote_score.tsv
            done
          done
        done
      done
    done
  done
done
