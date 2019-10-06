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

for t in mfo
do
  for fold in 0 1 2 3 4
  do
    for whiten in -w " "
    do
      if [ "$whiten" == "-w" ]; then
        cur_path=${nfold_root}/$t/fold$fold/${data_root}/[n_c]/w
        model_path=${nfold_root}/$t/fold$fold/${data_root}/1/w
      else
        cur_path=${nfold_root}/$t/fold$fold/${data_root}/[n_c]/nw
        model_path=${nfold_root}/$t/fold$fold/${data_root}/1/nw
      fi
      for explain in ${ratio_array}
      do
        if [ "$whiten" == "-w" ]; then
          output_path=${nfold_root}/$t/fold$fold/${data_root}/${explain}/w
        else
          output_path=${nfold_root}/$t/fold$fold/${data_root}/${explain}/nw
        fi
        # Non-redundant
        # seq_eval(matlab_path, cat, ont_db_path, oa_file, pred_file, benchmark_file, output_folder)
        if [ ! -f ${output_path}/nr/fmax.txt ]
        then
          matlab -nodisplay -r "addpath('./cafa2_eval/myscript');\
          seq_eval('./cafa2_eval/matlab','$t','./data/go_20130615-termdb.obo',\
          '${nfold_root}/$t/fold$fold/test_pro.txt',\
          '${output_path}/nr/vote_score.tsv',\
          '${nfold_root}/$t/fold$fold/test_ID.txt',\
          '${output_path}/nr/');quit;"
        fi
        # Redundant
        # seq_eval(matlab_path, cat, ont_db_path, oa_file, pred_file, benchmark_file, output_folder)
        if [ ! -f ${output_path}/r/fmax.txt ]
        then
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
