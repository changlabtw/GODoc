#!/bin/bash
# collect PCA experiment result by TFPSSM 1NN
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
echo type,fold,ratio,whiten,svd,fmax,precision,recall,tau >> ${output}

for type in ${target_type}
do
  for fold in 0 1 2 3 4
  do
    for ratio in 0.9 0.905 0.91 0.915 0.92 0.925 0.93 0.935 0.94 0.945 0.95 0.955 0.96 0.965 0.97 0.975 0.98 0.985
    do
      for whiten in w nw
      do
        for svd in r nr
        do
          res=${nfold_root}/${type}/fold${fold}/${data_root}/${ratio}/${whiten}/${svd}/fmax.txt
          if [ ! -f ${res} ]
          then
            echo "${res} not found!"
          else
            echo -n ${type},${fold},${ratio},${whiten},${svd}, | tail -n 1 -q - ${res} >> ${output}
          fi
        done
      done
    done
  done
done
