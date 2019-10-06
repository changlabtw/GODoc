#!/bin/bash
# take pca from 97.5% with whiten and Non-redundant in uniprot
for t in cco
do
  for fold in 0 1 2 3 4
  do
    mkdir thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/exp_knn
    for pca_r in r nr #for pca
    do
      mkdir thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/exp_knn/${pca_r}
      for p in 25 50 75
      do
        mkdir thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/exp_knn/${pca_r}/${p}
        output_path=thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/exp_knn/${pca_r}/${p}
        pca_path=thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/exp/0.975/w/${pca_r}
        # Non-redundant for knn
        mkdir thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/exp_knn/${pca_r}/${p}/nr
        python python/knn/dynamic_knn.py -b ${pca_path}/nr_pca.csv \
                                         -train ${pca_path}/train_tfpssm_pca.csv \
                                         -test ${pca_path}/test_tfpssm_pca.csv \
                                         -t ${p}% -o ${output_path}/nr/knn_res.tsv
        for lt in pro leaf
        do
          mkdir thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/exp_knn/${pca_r}/${p}/nr/${lt}
          cur_path=thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/exp_knn/${pca_r}/${p}/nr/${lt}
          python python/leafVote/leafVote.py -i ${output_path}/nr/knn_res.tsv -b \
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
        # Redundant for knn
        mkdir thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/exp_knn/${pca_r}/${p}/r
        python python/knn/dynamic_knn.py -b ${pca_path}/train_tfpssm_pca.csv \
                                         -train ${pca_path}/train_tfpssm_pca.csv \
                                         -test ${pca_path}/test_tfpssm_pca.csv \
                                         -t ${p}% -o ${output_path}/r/knn_res.tsv
        for lt in pro leaf
        do
          mkdir thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/exp_knn/${pca_r}/${p}/r/${lt}
          cur_path=thesis/data/uniprot/cafa2_train/nfold/$t/fold$fold/exp_knn/${pca_r}/${p}/r/${lt}
          python python/leafVote/leafVote.py -i ${output_path}/r/knn_res.tsv -b \
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
