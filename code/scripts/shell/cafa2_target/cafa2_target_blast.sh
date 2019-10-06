#!/bin/bash
mkdir thesis/data/cafa2_target/blast
for t in bpo cco mfo
do
  for bt in 1 2
  do
    nextflow blast_pred.nf \
    --query $PWD/thesis/data/cafa2_target/cafa2_target.fasta \
    --train $PWD/thesis/data/cafa2_train/cafa2_train.fasta \
    --output $PWD/thesis/data/cafa2_target/blast/${t}_type${bt} \
    --cat $t \
    --ont_db_path $PWD/data/go_20130615-termdb.obo \
    --test_oa_file $PWD/thesis/data/cafa2_target/pro_$t.txt \
    --train_oa_file $PWD/thesis/data/cafa2_train/leaf_$t.txt \
    --benchmark $PWD/cafa2_eval/benchmark/lists/${t}_all_type${bt}.txt
  done
done
