params.query = ""
params.output = "$PWD/tfpssm/"
params.d = 13
params.chunkSize = 1

/*
 * Initialization
 */

if ( params.query == "" ){
  error "--query should be set."
}

psiBlastResult_folder = file(params.query)
if( !psiBlastResult_folder.exists() ){
  error "No PSI-BLAST result folder: ${psiBlastResult_folder}."
}

tfpssm_folder = file(params.output)
if( !tfpssm_folder.exists() ){
  tfpssm_folder.mkdirs()
}

/*
 * Do tfpssm
 */

Channel
  .fromPath("${psiBlastResult_folder}/*.txt")
  .filter(){
    it -> file(it).getBaseName() != 'noresult'
  }
  .set { results }

process tfpssm {

  input:
    set file(result) from results

  output:
    set id, file('m_tfpssm'), t_state into m_tfpssms

  script:
    id = result.getBaseName()

    //check tfpssm exists
    if( file("${tfpssm_folder}/${id}.txt").exists() ){
      t_state = "exists"
    }
    else{
      t_state = "execute"
    }
    if( t_state == "exists" )
      """
      printf "exists" > m_tfpssm
      """
    else
      """
      pssm2tfpssm $result m_tfpssm $params.d
      """
}

m_tfpssms.subscribe{
  if ( it[2] == "exists" ){
    println "${it[0]}.txt already exists."
  }
  else{
    it[1].moveTo("${tfpssm_folder}/${it[0]}.txt")
    println "Save tfpssm result to ${tfpssm_folder}/${it[0]}.txt"
  }
}
