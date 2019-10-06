#!/bin/bash
# prepare PCA model
if [ "$#" -ne 3 ]; then
    echo "Illegal number of parameters, must eqal 3."
    echo "Usage: ./pca_tfpssm_prepare.sh [nfold folder root] [tfpssm folder] [data folder root]"
    exit
fi
echo nfold folder root: ${1}
echo tfpssm folder: ${2}
echo data folder root: ${3}

nfold_root=${1}
tfpssm_folder=${2}
data_root=${3}

for t in bpo
do
  for fold in 0 1 2 3 4
  do
    mkdir ${nfold_root}/$t/fold$fold/${data_root}
    for explain in 1
    do
      mkdir ${nfold_root}/$t/fold$fold/${data_root}/${explain}
      mkdir ${nfold_root}/$t/fold$fold/${data_root}/${explain}/w
      mkdir ${nfold_root}/$t/fold$fold/${data_root}/${explain}/nw
      mkdir ${nfold_root}/$t/fold$fold/${data_root}/${explain}/w/nr
      mkdir ${nfold_root}/$t/fold$fold/${data_root}/${explain}/w/r
      mkdir ${nfold_root}/$t/fold$fold/${data_root}/${explain}/nw/nr
      mkdir ${nfold_root}/$t/fold$fold/${data_root}/${explain}/nw/r
      for whiten in -w " "
      do
        if [ "$whiten" == "-w" ]; then
          cur_path=${nfold_root}/$t/fold$fold/${data_root}/${explain}/w
        else
          cur_path=${nfold_root}/$t/fold$fold/${data_root}/${explain}/nw
        fi
        # Non-redundant
        python python/pca/pca_folder.py -i ${tfpssm_folder} -n $explain $whiten\
                                    -l ${nfold_root}/$t/fold$fold/train_nr_ID.txt -list \
                                    -o ${cur_path}/nr/nr_pca.csv \
                                    -om ${cur_path}/nr/nr_pca_model.pkl
        python python/pca/pca_folder.py -i ${tfpssm_folder} -n $explain $whiten \
                                    -l ${nfold_root}/$t/fold$fold/train_ID.txt -list \
                                    -m ${cur_path}/nr/nr_pca_model.pkl \
                                    -o ${cur_path}/nr/train_tfpssm_pca.csv
        python python/pca/pca_folder.py -i ${tfpssm_folder} -n $explain $whiten \
                                    -l ${nfold_root}/$t/fold$fold/test_ID.txt -list \
                                    -m ${cur_path}/nr/nr_pca_model.pkl \
                                    -o ${cur_path}/nr/test_tfpssm_pca.csv
        # Redundant
        python python/pca/pca_folder.py -i ${tfpssm_folder} -n $explain $whiten \
                                    -l ${nfold_root}/$t/fold$fold/train_ID.txt -list \
                                    -o ${cur_path}/r/train_tfpssm_pca.csv \
                                    -om ${cur_path}/r/pca_model.pkl
        python python/pca/pca_folder.py -i ${tfpssm_folder} -n $explain $whiten \
                                    -l ${nfold_root}/$t/fold$fold/test_ID.txt -list \
                                    -m ${cur_path}/r/pca_model.pkl \
                                    -o ${cur_path}/r/test_tfpssm_pca.csv
      done
    done
  done
done
