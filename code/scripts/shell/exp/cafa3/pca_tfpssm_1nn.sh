#!/bin/bash
for t in cco
do
  for fold in 0 1 2 3 4
  do
    mkdir thesis/data/cafa3_train/nfold/$t/fold$fold/exp
    for explain in 1
    do
      mkdir thesis/data/cafa3_train/nfold/$t/fold$fold/exp/${explain}
      mkdir thesis/data/cafa3_train/nfold/$t/fold$fold/exp/${explain}/w
      mkdir thesis/data/cafa3_train/nfold/$t/fold$fold/exp/${explain}/nw
      mkdir thesis/data/cafa3_train/nfold/$t/fold$fold/exp/${explain}/w/nr
      mkdir thesis/data/cafa3_train/nfold/$t/fold$fold/exp/${explain}/w/r
      mkdir thesis/data/cafa3_train/nfold/$t/fold$fold/exp/${explain}/nw/nr
      mkdir thesis/data/cafa3_train/nfold/$t/fold$fold/exp/${explain}/nw/r
      for whiten in -w " "
      do
        if [ "$whiten" == "-w" ]; then
          cur_path=thesis/data/cafa3_train/nfold/$t/fold$fold/exp/${explain}/w
        else
          cur_path=thesis/data/cafa3_train/nfold/$t/fold$fold/exp/${explain}/nw
        fi
        # Non-redundant
        python python/pca/pca_folder.py -i thesis/data/cafa3_train/tfpssm/ -n $explain $whiten\
                                    -l thesis/data/cafa3_train/nfold/$t/fold$fold/train_nr_ID.txt -list \
                                    -o ${cur_path}/nr/nr_pca.csv \
                                    -om ${cur_path}/nr/nr_pca_model.pkl
        python python/pca/pca_folder.py -i thesis/data/cafa3_train/tfpssm/ -n $explain $whiten \
                                    -l thesis/data/cafa3_train/nfold/$t/fold$fold/train_ID.txt -list \
                                    -m ${cur_path}/nr/nr_pca_model.pkl \
                                    -o ${cur_path}/nr/train_tfpssm_pca.csv
        python python/pca/pca_folder.py -i thesis/data/cafa3_train/tfpssm/ -n $explain $whiten \
                                    -l thesis/data/cafa3_train/nfold/$t/fold$fold/test_ID.txt -list \
                                    -m ${cur_path}/nr/nr_pca_model.pkl \
                                    -o ${cur_path}/nr/test_tfpssm_pca.csv
        nextflow oneNN.nf --train_vec ${cur_path}/nr/train_tfpssm_pca.csv \
                          --train_label thesis/data/cafa3_train/nfold/$t/fold$fold/train_leaf.txt \
                          --test_vec ${cur_path}/nr/test_tfpssm_pca.csv \
                          --cat $t \
                          --ont_db_path $PWD/data/go_20130615-termdb.obo \
                          --oa_file $PWD/thesis/data/cafa3_train/nfold/$t/fold$fold/test_pro.txt \
                          --benchmark $PWD/thesis/data/cafa3_train/nfold/$t/fold$fold/test_ID.txt \
                          --output ${cur_path}/nr/tfpssm_1nn/
        # Redundant
        python python/pca/pca_folder.py -i thesis/data/cafa3_train/tfpssm/ -n $explain $whiten \
                                    -l thesis/data/cafa3_train/nfold/$t/fold$fold/train_ID.txt -list \
                                    -o ${cur_path}/r/train_tfpssm_pca.csv \
                                    -om ${cur_path}/r/pca_model.pkl
        python python/pca/pca_folder.py -i thesis/data/cafa3_train/tfpssm/ -n $explain $whiten \
                                    -l thesis/data/cafa3_train/nfold/$t/fold$fold/test_ID.txt -list \
                                    -m ${cur_path}/r/pca_model.pkl \
                                    -o ${cur_path}/r/test_tfpssm_pca.csv
        nextflow oneNN.nf --train_vec ${cur_path}/r/train_tfpssm_pca.csv \
                          --train_label thesis/data/cafa3_train/nfold/$t/fold$fold/train_leaf.txt \
                          --test_vec ${cur_path}/r/test_tfpssm_pca.csv \
                          --cat $t \
                          --ont_db_path $PWD/data/go_20130615-termdb.obo \
                          --oa_file $PWD/thesis/data/cafa3_train/nfold/$t/fold$fold/test_pro.txt \
                          --benchmark $PWD/thesis/data/cafa3_train/nfold/$t/fold$fold/test_ID.txt \
                          --output ${cur_path}/r/tfpssm_1nn/
      done
    done
  done
done
