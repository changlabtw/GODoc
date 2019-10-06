#!/bin/bash
for t in bpo cco mfo
do
  for p in 25 50 75
  do
    python python/knn/dynamic_knn.py -b thesis/data/cafa2_target/tfpssm_1nn/${t}_type1/cafa2_train_nr_pca.csv \
                                     -train thesis/data/cafa2_target/tfpssm_1nn/${t}_type1/train_tfpssm_pca.csv \
                                     -test thesis/data/cafa2_target/tfpssm_1nn/${t}_type1/test_tfpssm_pca.csv \
                                     -t ${p}% -o thesis/data/cafa2_target/knn_${t}_${p}_res.tsv
    python python/cath/ff_filter.py -i thesis/data/cafa2_target/knn_${t}_${p}_res.tsv \
                                    -test_m thesis/data/cafa2_target/cafa2_target_ff_ind.pkl \
                                    -train_m thesis/data/cafa2_train/cafa2_train_ff_ind.pkl \
                                    -o thesis/data/cafa2_target/knn_${t}_${p}_filtered_res.tsv
    for lt in pro leaf
    do
      for bt in 1 2
      do
        mkdir thesis/data/cafa2_target/${lt}_cathvote
        mkdir thesis/data/cafa2_target/${lt}_cathvote/${t}_type${bt}
        mkdir thesis/data/cafa2_target/${lt}_cathvote/${t}_type${bt}/${p}
        python python/cath/cath_vote_multi.py -i thesis/data/cafa2_target/knn_${t}_${p}_filtered_res.tsv \
                                              -l thesis/data/cafa2_train/${lt}_${t}.txt \
                                              -m 2 -o thesis/data/cafa2_target/${lt}_cathvote/${t}_type${bt}/${p}/cathvote_score.tsv
        # seq_eval(matlab_path, cat, ont_db_path, oa_file, pred_file, benchmark_file, output_folder)
        matlab -nodisplay -r "addpath('./cafa2_eval/myscript');\
        seq_eval('./cafa2_eval/matlab','$t','./data/go_20130615-termdb.obo',\
        './thesis/data/cafa2_target/pro_$t.txt',\
        './thesis/data/cafa2_target/${lt}_cathvote/${t}_type${bt}/${p}/cathvote_score.tsv',\
        './cafa2_eval/benchmark/lists/${t}_all_type${bt}.txt',\
        './thesis/data/cafa2_target/${lt}_cathvote/${t}_type${bt}/${p}');quit;"
      done
    done
  done
done
