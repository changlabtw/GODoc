params.query = ""
params.output = ""
params.fix_k = "10"
params.dynamic_threshold = "50%"
params.pssm_db = "$PWD/pred_data/psiBlastResult/"
params.pca_model = "$PWD/pred_data/nr_pca_model.pkl"
params.base_1nn = "$PWD/pred_data/cafa3_1nn_res.tsv"
params.train_pca = "$PWD/pred_data/cafa3_pca.csv"
params.label = "$PWD/pred_data/cafa3_label.txt"

/*
 * Initialization
 */

query_file = file(params.query)
if( !query_file.exists() ){
  error "No sequence fasta file: ${query_file}."
}

pssm_db_folder = file(params.pssm_db)
if( !pssm_db_folder.exists() ){
  error "No pssm db folder: ${pssm_db_folder}."
}

pca_model_file = file(params.pca_model)
if( !pca_model_file.exists() ){
  error "No PCA model file: ${pca_model_file}."
}

base_1nn_file = file(params.base_1nn)
if( !base_1nn_file.exists() ){
  error "No base 1NN file: ${base_1nn_file}."
}

train_pca_file = file(params.train_pca)
if( !train_pca_file.exists() ){
  error "No PCA of training data file: ${train_pca_file}."
}

label_file = file(params.label)
if( !pca_model_file.exists() ){
  error "No label file: ${label_file}."
}

output_folder = file(params.output)
if( !output_folder.exists() ){
  output_folder.mkdirs()
}


/*
 * TFPSSM -> PCA -> Hybrid KNN -> Vote
 */

process predict {
  script:
  """
  nextflow $PWD/tfpssm_db.nf --pssm_db ${pssm_db_folder} --query ${query_file} --output ${output_folder}
  python $PWD/pca_folder.py -a -m ${pca_model_file} -i ${output_folder}/tfpssm/ -o ${output_folder}/pca_result.csv
  python $PWD/hybrid_knn.py -b ${base_1nn_file} -train ${train_pca_file} -test ${output_folder}/pca_result.csv -t ${params.dynamic_threshold} -k ${params.fix_k} -o ${output_folder}/knn.csv
  python $PWD/leafVote.py -i ${output_folder}/knn.csv -l ${label_file} -b -o ${output_folder}/vote_score.txt
  """

}
