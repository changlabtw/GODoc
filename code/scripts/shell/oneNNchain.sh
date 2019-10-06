#!/bin/sh

nextflow oneNN.nf --train_vec pca/cco/train_pca.csv \
                  --train_label data/labels/all_function-C.tsv \
                  --test_vec pca/cco/test_pca.csv \
                  --cat CCO \
                  --oa_file $PWD/cafa2_eval/benchmark/groundtruth/propagated_CCO.txt \
                  --benchmark $PWD/cafa2_eval/benchmark/lists/cco_all_type1.txt \
                  --output onenn/pca/cco_type1

nextflow oneNN.nf --train_vec pca/bpo/train_pca.csv \
                  --train_label data/labels/all_function-P.tsv \
                  --test_vec pca/bpo/test_pca.csv \
                  --cat BPO \
                  --oa_file $PWD/cafa2_eval/benchmark/groundtruth/propagated_BPO.txt \
                  --benchmark $PWD/cafa2_eval/benchmark/lists/bpo_all_type1.txt \
                  --output onenn/pca/bpo_type1

nextflow oneNN.nf --train_vec pca/mfo/train_pca.csv \
                  --train_label data/labels/all_function-F.tsv \
                  --test_vec pca/mfo/test_pca.csv \
                  --cat MFO \
                  --oa_file $PWD/cafa2_eval/benchmark/groundtruth/propagated_MFO.txt \
                  --benchmark $PWD/cafa2_eval/benchmark/lists/mfo_all_type1.txt \
                  --output onenn/pca/mfo_type1

nextflow oneNN.nf --train_vec pca/cco/train_pca.csv \
                  --train_label data/labels/all_function-C.tsv \
                  --test_vec pca/cco/test_pca.csv \
                  --cat CCO \
                  --oa_file $PWD/cafa2_eval/benchmark/groundtruth/propagated_CCO.txt \
                  --benchmark $PWD/cafa2_eval/benchmark/lists/cco_all_type2.txt \
                  --output onenn/pca/cco_type2

nextflow oneNN.nf --train_vec pca/bpo/train_pca.csv \
                  --train_label data/labels/all_function-P.tsv \
                  --test_vec pca/bpo/test_pca.csv \
                  --cat BPO \
                  --oa_file $PWD/cafa2_eval/benchmark/groundtruth/propagated_BPO.txt \
                  --benchmark $PWD/cafa2_eval/benchmark/lists/bpo_all_type2.txt \
                  --output onenn/pca/bpo_type2

nextflow oneNN.nf --train_vec pca/mfo/train_pca.csv \
                  --train_label data/labels/all_function-F.tsv \
                  --test_vec pca/mfo/test_pca.csv \
                  --cat MFO \
                  --oa_file $PWD/cafa2_eval/benchmark/groundtruth/propagated_MFO.txt \
                  --benchmark $PWD/cafa2_eval/benchmark/lists/mfo_all_type2.txt \
                  --output onenn/pca/mfo_type2
