#!/bin/bash
# collect CATH-KNN experiment result
if [ "$#" -ne 4 ]; then
    echo "Illegal number of parameters, must eqal 4."
    echo "Usage: ./cath_partial.sh [nfold folder root] [data folder root] [output] [target type]"
    exit
fi
echo nfold folder root: ${1}
echo data folder root: ${2}
echo output: ${3}
echo target type: ${4}

nfold_root=${1}
data_root=${2}
output=${3}
target_type=${4}

touch ${output}
echo type,fold,q,k,fmax,precision,recall,tau >> ${output}

for type in ${4}
do
  for fold in 0 1 2 3 4
  do
    for q in q2 q3
    do
      output_path=${nfold_root}/${type}/fold${fold}/${data_root}/cath_knn
      for lt in pro
      do
        for k in 1 2 3 4 5 6 7 8 9 10
        do
          hybrid_path=${output_path}/${q}_${k}
          cur_path=${hybrid_path}/pro/0
          res=${cur_path}/fmax.txt
          if [ ! -f ${res} ]
          then
            echo "${res} not found!"
          else
            echo -n ${type},${fold},${q},${k}, | tail -n 1 -q - ${res} >> ${output}
          fi
        done
      done
    done
  done
done
