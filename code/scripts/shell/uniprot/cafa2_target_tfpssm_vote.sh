#!/bin/bash
for t in bpo cco mfo
do
  for p in 75
  do
    python python/knn/dynamic_knn.py -b thesis/data/uniprot/cafa2_target/tfpssm_1nn/${t}_type1/cafa2_train_nr_pca.csv \
                                     -train thesis/data/uniprot/cafa2_target/tfpssm_1nn/${t}_type1/train_tfpssm_pca.csv \
                                     -test thesis/data/uniprot/cafa2_target/tfpssm_1nn/${t}_type1/test_tfpssm_pca.csv \
                                     -t ${p}% -o thesis/data/uniprot/cafa2_target/knn_${t}_${p}_res.tsv
    for lt in pro
    do
      for bt in 1
      do
        mkdir thesis/data/uniprot/cafa2_target/${lt}_vote
        mkdir thesis/data/uniprot/cafa2_target/${lt}_vote/${t}_type${bt}
        mkdir thesis/data/uniprot/cafa2_target/${lt}_vote/${t}_type${bt}/${p}
        python python/leafVote/leafVote.py -i thesis/data/uniprot/cafa2_target/knn_${t}_${p}_res.tsv \
                                           -l thesis/data/uniprot/cafa2_train/${lt}_${t}.txt \
                                           -s 0 -o thesis/data/uniprot/cafa2_target/${lt}_vote/${t}_type${bt}/${p}/vote_score.tsv
        # seq_eval(matlab_path, cat, ont_db_path, oa_file, pred_file, benchmark_file, output_folder)
        matlab -nodisplay -r "addpath('./cafa2_eval/myscript');\
        seq_eval('./cafa2_eval/matlab','$t','./data/go_20130615-termdb.obo',\
        './thesis/data/uniprot/cafa2_target/pro_$t.txt',\
        './thesis/data/uniprot/cafa2_target/${lt}_vote/${t}_type${bt}/${p}/vote_score.tsv',\
        './cafa2_eval/benchmark/lists/${t}_all_type${bt}.txt',\
        './thesis/data/uniprot/cafa2_target/${lt}_vote/${t}_type${bt}/${p}');quit;"
      done
    done
  done
done
