#!/bin/bash
# take pca from 97.5% with whiten and Non-redundant in uniprot
for t in cco
do
  for fold in 0 1 2 3 4
  do
    mkdir thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/knn
    for pca_r in r nr #for pca
    do
      mkdir thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/knn/${pca_r}
      pca_path=thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/exp/0.975/w/${pca_r}
      python python/knn/knn.py -k 10 -d True\
                               -train ${pca_path}/train_tfpssm_pca.csv \
                               -test ${pca_path}/test_tfpssm_pca.csv \
                               -o thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/knn/${pca_r}/10nn_res.tsv
      for k in 1 2 3 4 5 6 7 8 9 10
      do
        mkdir thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/knn/${pca_r}/${k}
        output_path=thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/knn/${pca_r}/${k}
        for lt in pro leaf
        do
          mkdir ${output_path}/${lt}
          cur_path=${output_path}/${lt}
          python python/leafVote/leafVote.py -i thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/knn/${pca_r}/10nn_res.tsv -k ${k} \
                                             -l thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/train_${lt}.txt \
                                             -s 0 -o ${cur_path}/vote_score.tsv
          # seq_eval(matlab_path, cat, ont_db_path, oa_file, pred_file, benchmark_file, output_folder)
          matlab -nodisplay -r "addpath('./cafa2_eval/myscript');\
          seq_eval('./cafa2_eval/matlab','$t','./data/go_20130615-termdb.obo',\
          './thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/test_pro.txt',\
          '${cur_path}/vote_score.tsv',\
          './thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/test_ID.txt',\
          '${cur_path}');quit;"
        done
      done
    done
  done
done
