#!/bin/bash
# Hybrid KNN Experiment
if [ "$#" -ne 4 ]; then
    echo "Illegal number of parameters, must eqal 4."
    echo "Usage: ./hybrid_knn.sh [nfold folder root] [data folder root] [output] [type]"
    exit
fi
echo nfold folder root: ${1}
echo data folder root: ${2}
echo output: ${3}
echo Type: ${4}

nfold_root=${1}
data_root=${2}
output=${3}
target_type=${4}

touch ${output}
echo type,fold,q,k,label,method,based,fmax,precision,recall,tau >> ${output}

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
              res=${hybrid_path}/${lt}/${method}/${based}/fmax.txt
              if [ ! -f ${res} ]
              then
                echo "${res} not found!"
              else
                echo -n ${t},${fold},${q},${k},${lt},${method},${based}, | tail -n 1 -q - ${res} >> ${output}
              fi
            done
          done
        done
      done
    done
  done
done
