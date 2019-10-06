#!/bin/bash
# PCA experiment
if [ "$#" -ne 3 ]; then
    echo "Illegal number of parameters, must eqal 3."
    echo "Usage: ./pca_tfpssm_exp.sh [nfold folder root] [tfpssm folder] [data folder root]"
    exit
fi
echo nfold folder root: ${1}
echo tfpssm folder: ${2}
echo data folder root: ${3}

nfold_root=${1}
tfpssm_folder=${2}
data_root=${3}
ratio_array='0.9 0.905 0.91 0.915 0.92 0.925 0.93 0.935 0.94 0.945 0.95 0.955 0.96 0.965 0.97 0.975 0.98 0.985'

for t in bpo
do
  for fold in 0 1 2 3 4
  do
    mkdir ${nfold_root}/$t/fold$fold/${data_root}
    for explain in ${ratio_array}
    do
      mkdir ${nfold_root}/$t/fold$fold/${data_root}/${explain}
      mkdir ${nfold_root}/$t/fold$fold/${data_root}/${explain}/w
      mkdir ${nfold_root}/$t/fold$fold/${data_root}/${explain}/nw
      mkdir ${nfold_root}/$t/fold$fold/${data_root}/${explain}/w/nr
      mkdir ${nfold_root}/$t/fold$fold/${data_root}/${explain}/w/r
      mkdir ${nfold_root}/$t/fold$fold/${data_root}/${explain}/nw/nr
      mkdir ${nfold_root}/$t/fold$fold/${data_root}/${explain}/nw/r
    done
    for whiten in -w " "
    do
      if [ "$whiten" == "-w" ]; then
        cur_path=${nfold_root}/$t/fold$fold/${data_root}/[n_c]/w
        model_path=${nfold_root}/$t/fold$fold/${data_root}/1/w
      else
        cur_path=${nfold_root}/$t/fold$fold/${data_root}/[n_c]/nw
        model_path=${nfold_root}/$t/fold$fold/${data_root}/1/nw
      fi
      # # Non-redundant
      # python python/pca/pca_exp_iterate.py -i ${tfpssm_folder} -n ${ratio_array} \
      #                             -l ${nfold_root}/$t/fold$fold/train_ID.txt -list \
      #                             -m ${model_path}/nr/nr_pca_model.pkl \
      #                             -o ${cur_path}/nr/train_tfpssm_pca.csv
      # python python/pca/pca_exp_iterate.py -i ${tfpssm_folder} -n ${ratio_array} \
      #                             -l ${nfold_root}/$t/fold$fold/test_ID.txt -list \
      #                             -m ${model_path}/nr/nr_pca_model.pkl \
      #                             -o ${cur_path}/nr/test_tfpssm_pca.csv
      # # Redundant
      # python python/pca/pca_exp_iterate.py -i ${tfpssm_folder} -n ${ratio_array} \
      #                             -l ${nfold_root}/$t/fold$fold/train_ID.txt -list \
      #                             -m ${model_path}/r/pca_model.pkl \
      #                             -o ${cur_path}/r/train_tfpssm_pca.csv
      # python python/pca/pca_exp_iterate.py -i ${tfpssm_folder} -n ${ratio_array} \
      #                             -l ${nfold_root}/$t/fold$fold/test_ID.txt -list \
      #                             -m ${model_path}/r/pca_model.pkl \
      #                             -o ${cur_path}/r/test_tfpssm_pca.csv
      for explain in ${ratio_array}
      do
        if [ "$whiten" == "-w" ]; then
          output_path=${nfold_root}/$t/fold$fold/${data_root}/${explain}/w
        else
          output_path=${nfold_root}/$t/fold$fold/${data_root}/${explain}/nw
        fi
        # Non-redundant
        # python python/knn/knn.py -k 1\
        #                          -train ${output_path}/nr/train_tfpssm_pca.csv \
        #                          -test ${output_path}/nr/test_tfpssm_pca.csv \
        #                          -o ${output_path}/nr/1nn_res.tsv
        # python python/1NN/1NN.py -i ${output_path}/nr/1nn_res.tsv \
        #                          -l ${nfold_root}/$t/fold$fold/train_leaf.txt \
        #                          -o ${output_path}/nr/vote_score.tsv
        if [ ! -f ${output_path}/nr/fmax.txt ]
        then
          # seq_eval(matlab_path, cat, ont_db_path, oa_file, pred_file, benchmark_file, output_folder)
          matlab -nodisplay -r "addpath('./cafa2_eval/myscript');\
          seq_eval('./cafa2_eval/matlab','$t','./data/go_20130615-termdb.obo',\
          '${nfold_root}/$t/fold$fold/test_pro.txt',\
          '${output_path}/nr/vote_score.tsv',\
          '${nfold_root}/$t/fold$fold/test_ID.txt',\
          '${output_path}/nr/');quit;"
        fi

        # Redundant
        # python python/knn/knn.py -k 1\
        #                          -train ${output_path}/r/train_tfpssm_pca.csv \
        #                          -test ${output_path}/r/test_tfpssm_pca.csv \
        #                          -o ${output_path}/r/1nn_res.tsv
        # python python/1NN/1NN.py -i ${output_path}/r/1nn_res.tsv \
        #                          -l ${nfold_root}/$t/fold$fold/train_leaf.txt \
        #                          -o ${output_path}/r/vote_score.tsv
        if [ ! -f ${output_path}/r/fmax.txt ]
        then
          # seq_eval(matlab_path, cat, ont_db_path, oa_file, pred_file, benchmark_file, output_folder)
          matlab -nodisplay -r "addpath('./cafa2_eval/myscript');\
          seq_eval('./cafa2_eval/matlab','$t','./data/go_20130615-termdb.obo',\
          '${nfold_root}/$t/fold$fold/test_pro.txt',\
          '${output_path}/r/vote_score.tsv',\
          '${nfold_root}/$t/fold$fold/test_ID.txt',\
          '${output_path}/r/');quit;"
        fi
      done
    done
  done
done
