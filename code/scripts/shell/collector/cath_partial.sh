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
echo type,fold,q,fmax,precision,recall,tau >> ${output}

for type in ${4}
do
  for fold in 0 1 2 3 4
  do
    for q in q1 q2 q3
    do
      cur_path=${nfold_root}/${type}/fold${fold}/${data_root}/cath/${q}
      res=${cur_path}/partial_fmax.txt
      if [ ! -f ${res} ]
      then
        echo "${res} not found!"
      else
        echo -n ${type},${fold},${q}, | tail -n 1 -q - ${res} >> ${output}
      fi
    done
  done
done
