#!/bin/bash
#for t in bpo cco mfo
for t in bpo mfo
do
  for fold in 0 1 2 3 4
  do
    mkdir thesis/data/cafa2_train/nfold/$t/fold$fold/cath_exp
    for thres in $(seq 5 30)
    do
      mkdir thesis/data/cafa2_train/nfold/$t/fold$fold/cath_exp/${thres}
      python python/cath/ff_filter.py -i thesis/data/cafa2_train/nfold/$t/fold$fold/knn_75_res.tsv \
                                      -test_m thesis/data/cafa2_train/cafa2_train_ff_ind.pkl \
                                      -train_m thesis/data/cafa2_train/cafa2_train_ff_ind.pkl \
                                      -t 1.0e-${thres} \
                                      -o thesis/data/cafa2_train/nfold/$t/fold$fold/cath_exp/${thres}/knn_filtered_res.tsv
      python python/cath/cath_vote_multi.py -i thesis/data/cafa2_train/nfold/$t/fold$fold/cath_exp/${thres}/knn_filtered_res.tsv \
                                            -l thesis/data/cafa2_train/nfold/$t/fold$fold/train_pro.txt \
                                            -m 2 -o thesis/data/cafa2_train/nfold/$t/fold$fold/cath_exp/${thres}/cathvote_score.tsv
      # seq_eval(matlab_path, cat, ont_db_path, oa_file, pred_file, benchmark_file, output_folder)
      matlab -nodisplay -r "addpath('./cafa2_eval/myscript');\
      seq_eval('./cafa2_eval/matlab','$t','./data/go_20130615-termdb.obo',\
      './thesis/data/cafa2_train/nfold/$t/fold$fold/test_pro.txt',\
      './thesis/data/cafa2_train/nfold/$t/fold$fold/cath_exp/${thres}/cathvote_score.tsv',\
      './thesis/data/cafa2_train/nfold/$t/fold$fold/test_ID.txt',\
      './thesis/data/cafa2_train/nfold/$t/fold$fold/cath_exp/${thres}');quit;"
    done
  done
done
