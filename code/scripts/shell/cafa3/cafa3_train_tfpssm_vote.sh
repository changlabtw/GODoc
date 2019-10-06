#!/bin/bash
for t in bpo cco mfo
do
  for fold in 0 1 2 3 4
  do
    for p in 25 50 75
    do
      python python/knn/dynamic_knn.py -b thesis/data/cafa3_train/nfold/$t/fold$fold/train_tfpssm_pca.csv \
                                       -train thesis/data/cafa3_train/nfold/$t/fold$fold/train_tfpssm_pca.csv \
                                       -test thesis/data/cafa3_train/nfold/$t/fold$fold/test_tfpssm_pca.csv \
                                       -t ${p}% -o thesis/data/cafa3_train/nfold/$t/fold$fold/knn_${p}_res.tsv
      for lt in pro leaf
      do
        mkdir thesis/data/cafa3_train/nfold/$t/fold$fold/${lt}_vote
        mkdir thesis/data/cafa3_train/nfold/$t/fold$fold/${lt}_vote/${p}
        python python/leafVote/leafVote.py -i thesis/data/cafa3_train/nfold/$t/fold$fold/knn_${p}_res.tsv \
                                           -l thesis/data/cafa3_train/nfold/$t/fold$fold/train_${lt}.txt \
                                           -s 0 -o thesis/data/cafa3_train/nfold/$t/fold$fold/${lt}_vote/${p}/vote_score.tsv
        # seq_eval(matlab_path, cat, ont_db_path, oa_file, pred_file, benchmark_file, output_folder)
        matlab -nodisplay -r "addpath('./cafa2_eval/myscript');\
        seq_eval('./cafa2_eval/matlab','$t','./data/go_20160601-termdb.obo',\
        './thesis/data/cafa3_train/nfold/$t/fold$fold/test_pro.txt',\
        './thesis/data/cafa3_train/nfold/$t/fold$fold/${lt}_vote/${p}/vote_score.tsv',\
        './thesis/data/cafa3_train/nfold/$t/fold$fold/test_ID.txt',\
        './thesis/data/cafa3_train/nfold/$t/fold$fold/${lt}_vote/${p}');quit;"
      done
    done
  done
done
