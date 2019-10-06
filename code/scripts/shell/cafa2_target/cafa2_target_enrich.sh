#!/bin/bash
for t in bpo cco mfo
do
  for p in 75
  do
    for lt in pro
    do
      for bt in 1 2
      do
        mkdir thesis/data/cafa2_target/${lt}_enrich_cathvote
        mkdir thesis/data/cafa2_target/${lt}_enrich_cathvote/${t}_type${bt}
        mkdir thesis/data/cafa2_target/${lt}_enrich_cathvote/${t}_type${bt}/${p}
        python python/gorelation/enrich.py -i thesis/data/cafa2_target/${lt}_cathvote/${t}_type${bt}/${p}/cathvote_score.tsv\
                                           -r thesis/data/cafa2_train/${t}_rel.tsv \
                                           -o thesis/data/cafa2_target/${lt}_enrich_cathvote/${t}_type${bt}/${p}/cathvote_enrich_score.tsv

        # seq_eval(matlab_path, cat, ont_db_path, oa_file, pred_file, benchmark_file, output_folder)
        matlab -nodisplay -r "addpath('./cafa2_eval/myscript');\
        seq_eval('./cafa2_eval/matlab','$t','./data/go_20130615-termdb.obo',\
        './thesis/data/cafa2_target/pro_$t.txt',\
        './thesis/data/cafa2_target/${lt}_enrich_cathvote/${t}_type${bt}/${p}/cathvote_enrich_score.tsv',\
        './cafa2_eval/benchmark/lists/${t}_all_type${bt}.txt',\
        './thesis/data/cafa2_target/${lt}_enrich_cathvote/${t}_type${bt}/${p}');quit;"
      done
    done
  done
done
