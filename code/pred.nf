blast_cmd="psiblast -matrix BLOSUM80 -evalue 1e-5 -gapopen 9 -gapextend 2 -threshold 999 -seg yes -soft_masking true -num_iterations 3"

//params.db = ""  set db at nextflow.config
params.dataset = ""
params.psiBlastResult = "${params.dataset}/psiBlastResult/"
params.report = "noresult.txt" //append protein id if no PSI-BLAST result
params.tfpssm = "${params.dataset}/tfpssm/"
params.query = ""
params.label = ""
params.output = "results/"
params.model = ""
params.modelLabel = ""
params.chunkSize = 1
params.CA_dim = 36
params.output = "results/"

def haveResult(def result){
  myFile = file(result)
  count = 0
  myFile.eachLine {
    count++
  }
  if( count > 1){
    return true
  }
  else{
    return false
  }
}

/*
 * Initialization
 */

DB = params.db
if ( DB == null ){
  error "DB of BLAST must be set."
}

if( params.query == "" ){
  error "--query must be set."
}
else{
  query_file = file(params.query)
  if( !query_file.exists() ){
    error "No sequence fasta file: ${query_file}."
  }
}

if( params.model == "" ){
  error "--model must be set."
}
else{
  model_file = file(params.model)
  if( !model_file.exists() ){
    error "No model file: ${model_file}."
  }
}

if( params.modelLabel == ""){
  error "--modelLable must be set."
}
else{
  modelLabel_file = file(params.modelLabel)
  if( !modelLabel_file.exists() ){
    error "No model label file: ${modelLabel_file}."
  }
}

if( params.dataset == "" ){
  println "No dataset for PSI-BLAST result and tfpssm, the PSI-BLAST result and tfpssm will save at output folder."
}
else{
  dataset_folder = file("${params.dataset}")
  if( !dataset_folder.exists() ){
    error "No dataset: ${params.dataset} folder at ${params.dataset}."
  }
}

if( params.label == "" ){
  println "No label file for measurement."
}
else{
  label_file = file(params.label)
  if( !label_file.exists() ){
    error "No label tsv file: ${label_file}"
  }
}

output_folder = file(params.output)
if( output_folder.exists() ){
  output_folder.mkdirs()
}

if( params.dataset == "" ){
  psiBlastResult_folder = file("${output_folder}/psiBlastResult/")
  if( !psiBlastResult_folder.exists() ){
    psiBlastResult_folder.mkdirs()
  }

  report_file = file("${psiBlastResult_folder}/${params.report}")
  if( !report_file.exists() ){
    report_file.append('')
  }

  tfpssm_folder = file("${output_folder}/tfpssm/")
  if( !tfpssm_folder.exists() ){
    tfpssm_folder.mkdirs()
  }
}
else{
  psiBlastResult_folder = file(params.psiBlastResult)
  if( !psiBlastResult_folder.exists() ){
    error "No PSI-BLAST result folder: ${psiBlastResult_folder} folder."
  }

  report_file = file("${psiBlastResult_folder}/${params.report}")
  if( !report_file.exists() ){
    error "No PSI-BLAST noresult.txt: ${report_file}."
  }

  tfpssm_folder = file(params.tfpssm)
  if( !tfpssm_folder.exists() ){
    error "No tfpssm: ${tfpssm_folder} folder."
  }
}


/*
 * Split sequence FASTA file
 */

Channel
  .fromPath(query_file)
  .splitFasta( record: [id: true, seqString: true], by: params.chunkSize)
  .set { seq }

/*
 * Execute a PSI-BLAST job for each chunk for the provided sequences
 * If the PSI-BLAST result already exists, the state will be exists
 * and nothing will be copy to psiBlastResult folder.
 * If the sequence does'n have a PSI-BLAST result, the output text
 * file content will only have the sequence and the sequence ID will
 * be logged to noresult.txt at psiBlastResult folder.
 */

process blast {

    input:
      set( id, file('seq.fa') ) from seq

    output:
      set( id, file('out'), state ) into blast_result

    exec:
      if( file("${psiBlastResult_folder}/${id}.txt").exists() ){
        state = "exists"
      }
      else{
        state = "execute"
      }

    script:
      if( state == "exists" )
        """
        printf "exists" > out
        """
      else
        """
        $blast_cmd -db $DB -query seq.fa -out_ascii_pssm blastResult
        [ -f blastResult ] && cat blastResult > out || cat seq.fa > out
        """
}

process tfpssm {

  input:
    set( id, result, b_state ) from blast_result

  output:
    set( id, file('m_tfpssm'), t_state ) into m_tfpssms

  exec:
    //output PSI-BLAST result here
    if ( b_state == "exists" ){
      println "${id}.txt already exists."
    }
    else{
      if( haveResult(result) ){
        println "Save PSI-BLAST result to ${psiBlastResult_folder}/${id}.txt"
      }
      else{
        report_file.append("${id}\n")
        println "${id} doesn't have PSI-BLAST result."
      }
      result.moveTo("${psiBlastResult_folder}/${id}.txt")
    }
    result = file("${psiBlastResult_folder}/${id}.txt")

    //check tfpssm exists
    if( file("${tfpssm_folder}/${id}.txt").exists() ){
      t_state = "exists"
    }
    else{
      t_state = "execute"
    }

  script:
    if( t_state == "exists" )
      """
      printf "exists" > m_tfpssm
      """
    else
      """
      pssm2tfpssm $result m_tfpssm
      """

}

process merge {

  input:
    set( id, tfpssm, t_state ) from m_tfpssms

  output:
    file query_merge

  exec:
    if ( t_state == "exists" ){
      println "${id}.txt already exists."
    }
    else{
      tfpssm.moveTo("${tfpssm_folder}/${id}.txt")
      println "Save tfpssm result to ${tfpssm_folder}/${id}.txt"
    }
    tfpssm = file("${tfpssm_folder}/${id}.txt")

  script:
    """
    echo -ne ${id}, > query_merge
    cat ${tfpssm} >> query_merge
    """

}

query_merge_file = query_merge
                      .collectFile(name: "${output_folder}/query_merge")

process pred {
  input:
    file query_merge_file

  output:
    file pred_res
    file train_vec
    file test_vec

  exec:
    println "query_merge save at ${output_folder}/query_merge"

  script:
    if( params.label == "" ){
      """
      CA_pred.R ${model_file} ${modelLabel_file} ${query_merge_file} ${params.CA_dim}
      cat '1NN_res.tsv' > pred_res
      cat 'train_vec.tsv' > train_vec
      cat 'test_vec.tsv' > test_vec
      """
    }
    else{
      """
      CA_pred.R ${model_file} ${modelLabel_file} ${query_merge_file} ${params.CA_dim} ${label_file}
      cat '1NN_res.tsv' > pred_res
      cat 'train_vec.tsv' > train_vec
      cat 'test_vec.tsv' > test_vec
      """
    }

}

pred_res
  .subscribe{
    it.moveTo(output_folder)
  }
train_vec
  .subscribe{
    it.moveTo("${output_folder}/train_vec.tsv")
  }
test_vec
  .subscribe{
    it.moveTo("${output_folder}/test_vec.tsv")
  }
