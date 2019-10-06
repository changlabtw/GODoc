params.input = ""
params.output = "$PWD/hmm_results/"
params.msa = "clustal"
params.model = "data/hmmer/hmmmodels/fn3.hmm"
params.chunkSize = 1

/*
 * Initialization
 */

fasta_folder = file(params.input)
if( !fasta_folder.exists() ){
  error "No fasta folder: ${fasta_folder}."
}

hmm_model = file(params.model)
if( !hmm_model.exists() ){
  error "No hmm model: ${hmm_model}."
}

output_folder = file(params.output)
if( !output_folder.exists() ){
  output_folder.mkdirs()
}

hmm_folder = file("${params.output}/hmmbuild_results/")
if( !hmm_folder.exists() ){
  hmm_folder.mkdirs()
}

/*
 * Do hmmalign and hmmbuild
 */

Channel
  .fromPath("${fasta_folder}/*")
  .filter{
    it.text.length() - it.text.replace('>','').length() > 1
  }
  .set { fastas }

process hmmbuild {

  input:
    set file(fasta) from fastas

  output:
    set id, file('m_hmm'), state into m_hmms

  exec:
    id = fasta.getBaseName()
    go_id = id.split('_')[0]

    //check hmm exists
    if( file("${hmm_folder}/${id}.hmm").exists() ){
      state = "exists"
    }
    else{
      state = "execute"
    }

  script:
    if( state == "exists" )
      """
      printf "exists" > m_hmm
      """
    else
      if( params.msa == "hmmer" )
        """
        hmmalign ${hmm_model} ${fasta} > ${id}
        hmmbuild m_hmm ${id}
        """
      else if ( params.msa == "clustal" )
        """
        clustalo -i ${fasta} -o ${id}_msa --outfm=st
        hmmbuild -n ${go_id} --amino m_hmm ${id}_msa
        """
}

process merge {

  input:
    set( id, m_hmm, state ) from m_hmms

  output:
    file hmm_merge

  exec:
    if ( state == "exists" ){
      println "${id}.hmm already exists."
    }
    else{
      m_hmm.moveTo("${hmm_folder}/${id}.hmm")
      println "Save hmmalign result to ${hmm_folder}/${id}.hmm"
    }
    m_hmm = file("${hmm_folder}/${id}.hmm")

  script:
    """
    cat ${m_hmm} > hmm_merge
    """

}

hmm_merge_file = hmm_merge
                      .collectFile(name: "${output_folder}/hmm_merge")

process buildHMMDB {

  input:
    file hmm_merge_file

  output:
    file hmm_db
    file hmm_db_h3m
    file hmm_db_h3i
    file hmm_db_h3f
    file hmm_db_h3p

  exec:
    println "hmm_merge save at ${output_folder}/hmm_merge"

  script:
    """
    hmmpress ${hmm_merge_file}
    cat ${hmm_merge_file} > hmm_db
    cat ${hmm_merge_file}.h3m > hmm_db_h3m
    cat ${hmm_merge_file}.h3i > hmm_db_h3i
    cat ${hmm_merge_file}.h3f > hmm_db_h3f
    cat ${hmm_merge_file}.h3p > hmm_db_h3p
    ls
    """

}

hmm_db.subscribe{
  it.moveTo("${output_folder}/hmm_db")
  println "Save hmmpress result to ${output_folder}/hmm_db"
}
hmm_db_h3m.subscribe{
  it.moveTo("${output_folder}/hmm_db.h3m")
  println "Save hmmpress result to ${output_folder}/hmm_db.h3m"
}
hmm_db_h3i.subscribe{
  it.moveTo("${output_folder}/hmm_db.h3i")
  println "Save hmmpress result to ${output_folder}/hmm_db.h3i"
}
hmm_db_h3f.subscribe{
  it.moveTo("${output_folder}/hmm_db.h3f")
  println "Save hmmpress result to ${output_folder}/hmm_db.h3f"
}
hmm_db_h3p.subscribe{
  it.moveTo("${output_folder}/hmm_db.h3p")
  println "Save hmmpress result to ${output_folder}/hmm_db.h3p"
}
