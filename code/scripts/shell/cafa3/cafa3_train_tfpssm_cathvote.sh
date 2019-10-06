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
      python python/cath/ff_filter.py -i thesis/data/cafa3_train/nfold/$t/fold$fold/knn_${p}_res.tsv \
                                      -test_m thesis/data/cafa3_train/cafa3_train_ff_ind.pkl \
                                      -train_m thesis/data/cafa3_train/cafa3_train_ff_ind.pkl \
                                      -o thesis/data/cafa3_train/nfold/$t/fold$fold/knn_${p}_filtered_res.tsv
      for lt in pro leaf
      do
        mkdir thesis/data/cafa3_train/nfold/$t/fold$fold/${lt}_cathvote
        mkdir thesis/data/cafa3_train/nfold/$t/fold$fold/${lt}_cathvote/${p}
        python python/cath/cath_vote_multi.py -i thesis/data/cafa3_train/nfold/$t/fold$fold/knn_${p}_filtered_res.tsv \
                                              -l thesis/data/cafa3_train/nfold/$t/fold$fold/train_${lt}.txt \
                                              -m 2 -o thesis/data/cafa3_train/nfold/$t/fold$fold/${lt}_cathvote/${p}/cathvote_score.tsv
        # seq_eval(matlab_path, cat, ont_db_path, oa_file, pred_file, benchmark_file, output_folder)
        matlab -nodisplay -r "addpath('./cafa2_eval/myscript');\
        seq_eval('./cafa2_eval/matlab','$t','./data/go_20160601-termdb.obo',\
        './thesis/data/cafa3_train/nfold/$t/fold$fold/test_pro.txt',\
        './thesis/data/cafa3_train/nfold/$t/fold$fold/${lt}_cathvote/${p}/cathvote_score.tsv',\
        './thesis/data/cafa3_train/nfold/$t/fold$fold/test_ID.txt',\
        './thesis/data/cafa3_train/nfold/$t/fold$fold/${lt}_cathvote/${p}');quit;"
      done
    done
  done
done
