#!/bin/bash
# Fix fixed 1nn folder problem
if [ "$#" -ne 3 ]; then
    echo "Illegal number of parameters, must eqal 3."
    echo "Usage: ./fixed_knn.sh [nfold folder root] [data folder root] [type]"
    exit
fi
echo nfold folder root: ${1}
echo data folder root: ${2}
echo target type: ${3}

nfold_root=${1}
data_root=${2}
target_type=${3}

for t in ${target_type}
do
  for fold in 0
  do
    for k in 1 2 3 4 5 6 7 8 9 10
    do
      output_path=${nfold_root}/$t/fold$fold/${data_root}/${k}
      for lt in pro leaf
      do
        cur_path=${output_path}/${lt}
        if [ ! -f ${cur_path}/0/2/6/ ]
        then
          mv ${cur_path}/0/2/6/* ${cur_path}/6
          rm -r ${cur_path}/0/2/6/
        fi
        if [ ! -f ${cur_path}/0/2/ ]
        then
          mv ${cur_path}/0/2/* ${cur_path}/2
          rm -r ${cur_path}/0/2/
        fi
      done
    done
  done
done
