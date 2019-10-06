#!/bin/bash
for t in bpo cco mfo
do
  for fold in 0 1 2 3 4
  do
    nextflow blast_pred.nf \
    --query $PWD/thesis/data/cafa2_train/nfold/$t/fold$fold/test_seq.fasta \
    --train $PWD/thesis/data/cafa2_train/nfold/$t/fold$fold/train_seq.fasta \
    --output $PWD/thesis/data/cafa2_train/nfold/$t/fold$fold/blast \
    --cat $t \
    --ont_db_path $PWD/data/go_20130615-termdb.obo \
    --test_oa_file $PWD/thesis/data/cafa2_train/nfold/$t/fold$fold/test_pro.txt \
    --train_oa_file $PWD/thesis/data/cafa2_train/nfold/$t/fold$fold/train_leaf.txt \
    --benchmark $PWD/thesis/data/cafa2_train/nfold/$t/fold$fold/test_ID.txt
  done
done
