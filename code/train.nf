params.dataset = ""
params.tfpssm = "${params.dataset}/tfpssm/"
params.label = "${params.dataset}/function.tsv"
params.output = "results/"
params.fold_num = 5
params.chunkSize = 1

/*
 * Initialization
 */

 if ( (params.tfpssm == "${params.dataset}/tfpssm/") != (params.label == "${params.dataset}/function.tsv") ){
   error "--tfpssm and --label must be set same time."
 }

 if ( params.tfpssm == "${params.dataset}/tfpssm/" || params.label == "${params.dataset}/function.tsv"){
   dataset_folder = file("${params.dataset}")
   if( !dataset_folder.exists() ){
     error "No dataset: ${params.dataset} folder."
   }
 }

tfpssm_folder = file(params.tfpssm)
if( !tfpssm_folder.exists() ){
  error "No tfpssm: ${tfpssm_folder} folder."
}

label_file = file(params.label)
if( !label_file.exists() ){
  error "No label tsv file: ${label_file}."
}

output_folder = file(params.output)
if( !output_folder.exists() ){
  output_folder.mkdirs()
}

/*
 * Split label TSV file
 */

Channel
  .fromPath(label_file)
  .splitCsv(header: ['id','label'], sep:'\t', by: params.chunkSize ){ row -> row['id'] }
  .unique()
  .set { ids }

/*
 * Merge tfpssms into a single file
 */

process merge {

    input:
      set id from ids

    output:
      file tfpssm_merge

    exec:
      m_tfpssm = file("${tfpssm_folder}/${id}.txt")
      if( !m_tfpssm.exists() ){
        error "No ${id}.txt at ${tfpssm_folder}."
      }

    script:
      """
      echo -ne ${id}, > tfpssm_merge
      cat ${m_tfpssm} >> tfpssm_merge
      """
}

/*
 * Collect all the ftpssm vector to model_tfpssm_file
 */

 model_tfpssm_file = tfpssm_merge
                       .collectFile(name: "${output_folder}/model_tfpssm")

process modelCA  {
    echo true

    input:
      file model_tfpssm_file

    output:
      file nfold_res
      file pred_res
      file nlist

    exec:
      println "model_tfpssm save at ${output_folder}/model_tfpssm"

    script:
      """
      nfold.py ${label_file} nlist ${params.fold_num}
      CA_train.R ${model_tfpssm_file} ${label_file} ${params.fold_num} nlist > nfold_res
      cat nfold_res
      cat '1NN_res.tsv' > pred_res
      """
}

nfold_res
  .subscribe{
    it.moveTo(output_folder)
  }
pred_res
  .subscribe{
    it.moveTo(output_folder)
  }
nlist
  .subscribe{
    it.moveTo(output_folder)
  }
