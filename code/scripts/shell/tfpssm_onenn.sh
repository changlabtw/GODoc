#!/bin/bash

for i in $(seq 1 4)
do
  #BPO

  nextflow oneNN.nf --train_vec tfpssm_exp/tfpssm_$i/bpo_pca_result.csv \
                    --train_label data/labels/all_function-P.tsv \
                    --test_vec tfpssm_exp/tfpssm_$i/target.csv \
                    --cat BPO \
                    --oa_file $PWD/cafa2_eval/benchmark/groundtruth/propagated_BPO.txt \
                    --benchmark $PWD/cafa2_eval/benchmark/lists/bpo_all_type1.txt \
                    --output tfpssm_exp/tfpssm_$i/bpo_type1

  nextflow oneNN.nf --train_vec tfpssm_exp/tfpssm_$i/bpo_pca_result.csv \
                    --train_label data/labels/all_function-P.tsv \
                    --test_vec tfpssm_exp/tfpssm_$i/target.csv \
                    --cat BPO \
                    --oa_file $PWD/cafa2_eval/benchmark/groundtruth/propagated_BPO.txt \
                    --benchmark $PWD/cafa2_eval/benchmark/lists/bpo_all_type2.txt \
                    --output tfpssm_exp/tfpssm_$i/bpo_type2

  #CCO

  nextflow oneNN.nf --train_vec tfpssm_exp/tfpssm_$i/cco_pca_result.csv \
                    --train_label data/labels/all_function-C.tsv \
                    --test_vec tfpssm_exp/tfpssm_$i/target.csv \
                    --cat CCO \
                    --oa_file $PWD/cafa2_eval/benchmark/groundtruth/propagated_CCO.txt \
                    --benchmark $PWD/cafa2_eval/benchmark/lists/cco_all_type1.txt \
                    --output tfpssm_exp/tfpssm_$i/cco_type1

  nextflow oneNN.nf --train_vec tfpssm_exp/tfpssm_$i/cco_pca_result.csv \
                    --train_label data/labels/all_function-C.tsv \
                    --test_vec tfpssm_exp/tfpssm_$i/target.csv \
                    --cat CCO \
                    --oa_file $PWD/cafa2_eval/benchmark/groundtruth/propagated_CCO.txt \
                    --benchmark $PWD/cafa2_eval/benchmark/lists/cco_all_type2.txt \
                    --output tfpssm_exp/tfpssm_$i/cco_type2

  #MFO

  nextflow oneNN.nf --train_vec tfpssm_exp/tfpssm_$i/mfo_pca_result.csv \
                    --train_label data/labels/all_function-F.tsv \
                    --test_vec tfpssm_exp/tfpssm_$i/target.csv \
                    --cat MFO \
                    --oa_file $PWD/cafa2_eval/benchmark/groundtruth/propagated_MFO.txt \
                    --benchmark $PWD/cafa2_eval/benchmark/lists/mfo_all_type1.txt \
                    --output tfpssm_exp/tfpssm_$i/mfo_type1

  nextflow oneNN.nf --train_vec tfpssm_exp/tfpssm_$i/mfo_pca_result.csv \
                    --train_label data/labels/all_function-F.tsv \
                    --test_vec tfpssm_exp/tfpssm_$i/target.csv \
                    --cat MFO \
                    --oa_file $PWD/cafa2_eval/benchmark/groundtruth/propagated_MFO.txt \
                    --benchmark $PWD/cafa2_eval/benchmark/lists/mfo_all_type2.txt \
                    --output tfpssm_exp/tfpssm_$i/mfo_type2
done
