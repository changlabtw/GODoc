#!/bin/bash
# collect Fixed-KNN experiment result
if [ "$#" -ne 4 ]; then
    echo "Illegal number of parameters, must eqal 4."
    echo "Usage: ./pca_ratio.sh [nfold folder root] [data folder root] [output] [target type]"
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
echo type,fold,k,label,method,fmax,precision,recall,tau >> ${output}

for type in ${4}
do
  for fold in 0 1 2 3 4
  do
    for k in 1 2 3 4 5 6 7 8 9 10
    do
      for lt in pro leaf
      do
        cur_path=${nfold_root}/${type}/fold${fold}/${data_root}/${k}/${lt}
        for method in 0 2 6
        do
          res=${cur_path}/${method}/fmax.txt
          if [ ! -f ${res} ]
          then
            echo "${res} not found!"
          else
            echo -n ${type},${fold},${k},${lt},${method}, | tail -n 1 -q - ${res} >> ${output}
          fi
        done
      done
    done
  done
done
