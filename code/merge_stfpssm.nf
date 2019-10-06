params.dataset = ""
params.stfpssm = "${params.dataset}/stfpssm/"
params.label = "${params.dataset}/function.tsv"
params.output = "results"
params.chunkSize = 1

/*
 * Initialization
 */

if ( (params.stfpssm == "${params.dataset}/stfpssm/") != (params.label == "${params.dataset}/function.tsv") ){
  error "--stfpssm and --label must be set same time."
}

if ( params.stfpssm == "${params.dataset}/stfpssm/" || params.label == "${params.dataset}/function.tsv"){
  dataset_folder = file(params.dataset)
  if( !dataset_folder.exists() ){
    error "No dataset: ${params.dataset} folder."
  }
}

stfpssm_folder = file(params.stfpssm)
if( !stfpssm_folder.exists() ){
  error "No stfpssm: ${stfpssm_folder} folder."
}

label_file = file(params.label)
if( !label_file.exists() ){
  error "No label tsv file: ${label_file} folder."
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
 * Merge stfpssms into a single file
 */

process merge {

    maxForks 1

    input:
      set id from ids

    output:
      stdout channel

    exec:
      m_stfpssm = file("${stfpssm_folder}/${id}.txt")
      if( !m_stfpssm.exists() ){
        state = "skip"
        println "No ${id}.txt at ${stfpssm_folder}."
      }
      else{
        state = "execute"
      }

    script:
      if( state == "skip" ){
        """
        printf "skip" ${id}
        """
      }
      else if( state == "execute" ){
        """
        echo -ne ${id}, > m_stfpssm_merge
        cat ${m_stfpssm} >> m_stfpssm_merge
        cat m_stfpssm_merge >> ${output_folder}/model_stfpssm
        echo '' >> ${output_folder}/model_stfpssm
        """
      }
}

/*
 * Collect all the ftpssm vector to model_stfpssm_file
 */

// stfpssm_merge.collectFile( name: "${output_folder}/model_stfpssm" ) {
//   item ->
//     if(item[1] == "execute"){
//       return item[0].text + '\n'
//     }
// }
// channel.subscribe{
//   println it
// }
