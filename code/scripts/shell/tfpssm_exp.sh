#!/bin/bash

# for i in $(seq 1 12)
for i in 13
do
  #nextflow blastToTfpssm.nf --query data/all/psiBlastResult --output data/all/tfpssm_exp/tfpssm_$i/ --d $i
  #nextflow blastToTfpssm.nf --query data/target/psiBlastResult --output data/target/tfpssm_exp/tfpssm_$i/ --d $i
  #mkdir tfpssm_exp/tfpssm_$i
  #python python/pca/pca_folder.py -i data/all/tfpssm_exp/tfpssm_$i/ -l data/all/all_50_nr_ID.txt -list -o tfpssm_exp/tfpssm_$i/pca_result.csv -om tfpssm_exp/tfpssm_$i/pca_model.pkl
  #python python/pca/pca_folder.py -i data/all/tfpssm_exp/tfpssm_$i/ -a -m tfpssm_exp/tfpssm_$i/pca_model.pkl -o tfpssm_exp/tfpssm_$i/pca_result.csv
  #python python/pca/pca_folder.py -i data/target/tfpssm_exp/tfpssm_$i/ -a -m tfpssm_exp/tfpssm_$i/pca_model.pkl -o tfpssm_exp/tfpssm_$i/target.csv

  #BPO
  python python/pca/filter.py -i tfpssm_exp/tfpssm_$i/pca_result.csv -l data/labels/all_bpo_list.txt -o tfpssm_exp/tfpssm_$i/bpo_pca_result.csv

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
  python python/pca/filter.py -i tfpssm_exp/tfpssm_$i/pca_result.csv -l data/labels/all_cco_list.txt -o tfpssm_exp/tfpssm_$i/cco_pca_result.csv

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
  python python/pca/filter.py -i tfpssm_exp/tfpssm_$i/pca_result.csv -l data/labels/all_mfo_list.txt -o tfpssm_exp/tfpssm_$i/mfo_pca_result.csv

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
