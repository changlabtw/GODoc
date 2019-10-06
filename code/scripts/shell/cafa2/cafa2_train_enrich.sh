#!/bin/bash
for t in bpo cco mfo
do
  for fold in 0 1 2 3 4
  do
    for p in 75
    do
      for lt in pro
      do
        mkdir thesis/data/cafa2_train/nfold/$t/fold$fold/${lt}_enrich_cathvote
        mkdir thesis/data/cafa2_train/nfold/$t/fold$fold/${lt}_enrich_cathvote/${p}
        python python/gorelation/enrich.py -i thesis/data/cafa2_train/nfold/$t/fold$fold/${lt}_cathvote/${p}/cathvote_score.tsv\
                                           -r thesis/data/cafa2_train/${t}_rel.tsv \
                                           -o thesis/data/cafa2_train/nfold/$t/fold$fold/${lt}_enrich_cathvote/${p}/cathvote_enrich_score.tsv
        # seq_eval(matlab_path, cat, ont_db_path, oa_file, pred_file, benchmark_file, output_folder)
        matlab -nodisplay -r "addpath('./cafa2_eval/myscript');\
        seq_eval('./cafa2_eval/matlab','$t','./data/go_20130615-termdb.obo',\
        './thesis/data/cafa2_train/nfold/$t/fold$fold/test_pro.txt',\
        './thesis/data/cafa2_train/nfold/$t/fold$fold/${lt}_enrich_cathvote/${p}/cathvote_enrich_score.tsv',\
        './thesis/data/cafa2_train/nfold/$t/fold$fold/test_ID.txt',\
        './thesis/data/cafa2_train/nfold/$t/fold$fold/${lt}_enrich_cathvote/${p}');quit;"
      done
    done
  done
done
