#!/bin/bash
# collect baseline model result
if [ "$#" -ne 3 ]; then
    echo "Illegal number of parameters, must eqal 3."
    echo "Usage: ./baseline.sh [nfold folder root] [output] [type]"
    exit
fi
echo nfold folder root: ${1}
echo output: ${2}
echo target type: ${3}

nfold_root=${1}
output=${2}
target_type=${3}

touch ${output}
echo type,fold,model,fmax,precision,recall,tau >> ${output}

for type in ${target_type}
do
  for fold in 0 1 2 3 4
  do
    for m in blast naive_leaf
    do
      res=${nfold_root}/${type}/fold${fold}/${m}/fmax.txt
      if [ ! -f ${res} ]
      then
        echo "${res} not found!"
      else
        echo -n ${type},${fold},${m}, | tail -n 1 -q - ${res} >> ${output}
      fi
    done
  done
done
