#!/bin/bash
# PCA experiment
# PCA vector files must be [nfold_root]/pca/[explain_ratio]
if [ "$#" -ne 4 ]; then
    echo "Illegal number of parameters, must eqal 4."
    echo "Usage: ./fixed_knn.sh [nfold folder root] [data folder root] [PCA folder root] [PCA explain ratio]"
    exit
fi
echo nfold folder root: ${1}
echo data folder root: ${2}
echo PCA folder root: ${3}
echo PCA explain ratio: ${4}

nfold_root=${1}
data_root=${2}
pca_root=${3}
explain_ratio=${4}

for t in bpo
do
  for fold in 0 1 2 3 4
  do
    mkdir ${nfold_root}/$t/fold$fold/${data_root}
    pca_path=${nfold_root}/${t}/fold$fold/${pca_root}/${explain_ratio}/w/nr
    python python/knn/knn.py -k 10 -d True\
                             -train ${pca_path}/train_tfpssm_pca.csv \
                             -test ${pca_path}/test_tfpssm_pca.csv \
                             -o ${nfold_root}/$t/fold$fold/${data_root}/10nn_res.tsv
    for k in 1 2 3 4 5 6 7 8 9 10
    do
      mkdir ${nfold_root}/$t/fold$fold/${data_root}/${k}
      output_path=${nfold_root}/$t/fold$fold/${data_root}/${k}
      for lt in pro leaf
      do
        mkdir ${output_path}/${lt}
        for method in 0 2 6
        do
          cur_path=${output_path}/${lt}/${method}
          mkdir ${cur_path}
          python python/leafVote/leafVote.py -i ${nfold_root}/$t/fold$fold/${data_root}/10nn_res.tsv -k ${k} \
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
