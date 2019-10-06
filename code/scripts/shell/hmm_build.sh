#!/bin/bash

for t in cco bpo
do
  python python/hmm/filterGO.py -i data/pro_label/all_fun_pro_${t}.tsv -t p -p 0.95 -o hmm/${t}/GO_95_list.txt
  python python/hmm/buildFasta.py -f data/all/all.fasta -l data/labels/all_fun_leaf_${t}.tsv -g hmm/${t}/GO_95_list.txt -o hmm/${t}/fastas
  nextflow fastaClust.nf --input hmm/${t}/fastas/ --output hmm/${t}/clusters/ --nr hmm/${t}/nr/
  nextflow hmmClustBuild.nf --input hmm/${t}/clusters/ --output hmm/${t}/model/
  ./bin/hmmscan --tblout hmm/${t}/hmm_scan_result.txt hmm/${t}/model/hmm_db data/target/seq.fasta
done
