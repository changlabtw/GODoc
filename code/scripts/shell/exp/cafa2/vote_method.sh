#!/bin/bash
# take pca from 95% with whiten and Non-redundant in SWISS
for t in cco
do
  for fold in 0 1 2 3 4
  do
    for pca_r in r nr #for pca
    do
      for p in 25 50 75
      do
        output_path=thesis/data/cafa2_train/nfold/$t/fold$fold/exp_knn/${pca_r}/${p}
        for method in 6
        do
          # Non-redundant for knn
          for lt in pro leaf
          do
            mkdir thesis/data/cafa2_train/nfold/$t/fold$fold/exp_knn/${pca_r}/${p}/nr/${lt}_${method}
            cur_path=thesis/data/cafa2_train/nfold/$t/fold$fold/exp_knn/${pca_r}/${p}/nr/${lt}_${method}
            python python/leafVote/leafVote.py -i ${output_path}/nr/knn_res.tsv \
                                               -l thesis/data/cafa2_train/nfold/$t/fold$fold/train_${lt}.txt \
                                               -s ${method} -o ${cur_path}/vote_score.tsv
            # seq_eval(matlab_path, cat, ont_db_path, oa_file, pred_file, benchmark_file, output_folder)
            matlab -nodisplay -r "addpath('./cafa2_eval/myscript');\
            seq_eval('./cafa2_eval/matlab','$t','./data/go_20130615-termdb.obo',\
            './thesis/data/cafa2_train/nfold/$t/fold$fold/test_pro.txt',\
            '${cur_path}/vote_score.tsv',\
            './thesis/data/cafa2_train/nfold/$t/fold$fold/test_ID.txt',\
            '${cur_path}');quit;"
          done
          # Redundant for knn
          for lt in pro leaf
          do
            mkdir thesis/data/cafa2_train/nfold/$t/fold$fold/exp_knn/${pca_r}/${p}/r/${lt}_${method}
            cur_path=thesis/data/cafa2_train/nfold/$t/fold$fold/exp_knn/${pca_r}/${p}/r/${lt}_${method}
            python python/leafVote/leafVote.py -i ${output_path}/r/knn_res.tsv \
                                               -l thesis/data/cafa2_train/nfold/$t/fold$fold/train_${lt}.txt \
                                               -s ${method} -o ${cur_path}/vote_score.tsv
            # seq_eval(matlab_path, cat, ont_db_path, oa_file, pred_file, benchmark_file, output_folder)
            matlab -nodisplay -r "addpath('./cafa2_eval/myscript');\
            seq_eval('./cafa2_eval/matlab','$t','./data/go_20130615-termdb.obo',\
            './thesis/data/cafa2_train/nfold/$t/fold$fold/test_pro.txt',\
            '${cur_path}/vote_score.tsv',\
            './thesis/data/cafa2_train/nfold/$t/fold$fold/test_ID.txt',\
            '${cur_path}');quit;"
          done
        done
      done
    done
  done
done
