#!/bin/bash

for model in "$1"/*/
do
  echo ${model}
  for t in "$model"/*/
  do
    echo ${t}
    python python/pca/filter.py -i ${model}/pca_res.csv -l ${t}/ID_list.txt -o ${t}/pca_res.csv
    python python/pca/nfold_split.py -i ${t}/pca_res.csv -n 5 -o ${t}/nfold
    for fold in "$t"/nfold/*/
    do
      echo ${fold}
      cut -d, -f 1 ${fold}/test_pca.csv > ${fold}/test_ID_list.txt
      python python/knn/knn.py -train ${fold}/train_pca.csv -test ${fold}/test_pca.csv -t 0.00101 -d True -o ${fold}/knn_file.txt
      if [ ${t##*//} = "bpo/" ]
      then
        python python/leafVote/forceLeafVote.py -i ${fold}/knn_file.txt -l data/labels/all_function-P.tsv -o ${fold}/force
        for f in "$fold"/force/*
        do
          matlab -nodisplay -r "addpath('cafa2_eval/myscript');fmax('cafa2_eval/matlab','BPO','cafa2_eval/ontology/','data/labels/all_function-P.tsv','${f}','${fold}/test_ID_list.txt','${f}_pro_res_type1.txt');quit;"
        done
      elif [ ${t##*//} = "cco/" ]
      then
        python python/leafVote/forceLeafVote.py -i ${fold}/knn_file.txt -l data/labels/all_function-C.tsv -o ${fold}/force
        for f in "$fold"/force/*
        do
          matlab -nodisplay -r "addpath('cafa2_eval/myscript');fmax('cafa2_eval/matlab','CCO','cafa2_eval/ontology/','data/labels/all_function-C.tsv','${f}','${fold}/test_ID_list.txt','${f}_pro_res_type1.txt');quit;"
        done
      elif [ ${t##*//} = "mfo/" ]
      then
        python python/leafVote/forceLeafVote.py -i ${fold}/knn_file.txt -l data/labels/all_function-F.tsv -o ${fold}/force
        for f in "$fold"/force/*
        do
          matlab -nodisplay -r "addpath('cafa2_eval/myscript');fmax('cafa2_eval/matlab','MFO','cafa2_eval/ontology/','data/labels/all_function-F.tsv','${f}','${fold}/test_ID_list.txt','${f}_pro_res_type1.txt');quit;"
        done
      fi
    done
  done
done
