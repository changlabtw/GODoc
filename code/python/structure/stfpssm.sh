#!/bin/bash

for t in "sliced_folder"/*
do
  for file in "${t}"/*
  do
    name=$(basename ${file})
    name="${name%.*}"
    if [ $t = "sliced_folder/h" ]
    then
      pssm2tfpssm ${file} tfpssms/h/${name}.txt $1
    elif [ $t = "sliced_folder/e" ]
    then
      pssm2tfpssm ${file} tfpssms/e/${name}.txt $2
    elif [ $t = "sliced_folder/c" ]
    then
      pssm2tfpssm ${file} tfpssms/c/${name}.txt $3
    fi
  done
done
