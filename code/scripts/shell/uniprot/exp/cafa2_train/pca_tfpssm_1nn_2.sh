#!/bin/bash
for t in cco
do
  for fold in 0 1 2 3 4
  do
    mkdir thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/exp
    for explain in 0.9 0.915 0.92 0.925 0.93 0.935 0.94 0.945 0.95 0.955 0.96 0.965 0.97 0.975 0.98 0.985
    do
      mkdir thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/exp/${explain}
      mkdir thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/exp/${explain}/w
      mkdir thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/exp/${explain}/nw
      mkdir thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/exp/${explain}/w/nr
      mkdir thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/exp/${explain}/w/r
      mkdir thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/exp/${explain}/nw/nr
      mkdir thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/exp/${explain}/nw/r
      for whiten in -w " "
      do
        if [ "$whiten" == "-w" ]; then
          cur_path=thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/exp/${explain}/w
          model_path=thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/exp/1/w
        else
          cur_path=thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/exp/${explain}/nw
          model_path=thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/exp/1/nw
        fi
        # Non-redundant
        python python/pca/pca_exp.py -i thesis/data/uniprot/cafa2_train/tfpssm/ -n $explain \
                                    -l thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/train_ID.txt -list \
                                    -m ${model_path}/nr/nr_pca_model.pkl \
                                    -o ${cur_path}/nr/train_tfpssm_pca.csv
        python python/pca/pca_exp.py -i thesis/data/uniprot/cafa2_train/tfpssm/ -n $explain \
                                    -l thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/test_ID.txt -list \
                                    -m ${model_path}/nr/nr_pca_model.pkl \
                                    -o ${cur_path}/nr/test_tfpssm_pca.csv
        nextflow oneNN.nf --train_vec ${cur_path}/nr/train_tfpssm_pca.csv \
                          --train_label thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/train_leaf.txt \
                          --test_vec ${cur_path}/nr/test_tfpssm_pca.csv \
                          --cat $t \
                          --ont_db_path $PWD/data/go_20130615-termdb.obo \
                          --oa_file $PWD/thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/test_pro.txt \
                          --benchmark $PWD/thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/test_ID.txt \
                          --output ${cur_path}/nr/tfpssm_1nn/
        # Redundant
        python python/pca/pca_exp.py -i thesis/data/uniprot/cafa2_train/tfpssm/ -n $explain \
                                    -l thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/train_ID.txt -list \
                                    -o ${cur_path}/r/train_tfpssm_pca.csv \
                                    -m ${model_path}/r/pca_model.pkl
        python python/pca/pca_exp.py -i thesis/data/uniprot/cafa2_train/tfpssm/ -n $explain \
                                    -l thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/test_ID.txt -list \
                                    -m ${model_path}/r/pca_model.pkl \
                                    -o ${cur_path}/r/test_tfpssm_pca.csv
        nextflow oneNN.nf --train_vec ${cur_path}/r/train_tfpssm_pca.csv \
                          --train_label thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/train_leaf.txt \
                          --test_vec ${cur_path}/r/test_tfpssm_pca.csv \
                          --cat $t \
                          --ont_db_path $PWD/data/go_20130615-termdb.obo \
                          --oa_file $PWD/thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/test_pro.txt \
                          --benchmark $PWD/thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/test_ID.txt \
                          --output ${cur_path}/r/tfpssm_1nn/
      done
    done
  done
done
