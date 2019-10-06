params.dataset = ""
params.from = ""
params.to = ""
params.chunkSize = 1

/*
 * Initialization
 */

from_folder = file(params.from)
if( !from_folder.exists() ){
  error "No from folder: ${params.dataset}."
}

to_folder = file(params.to)
if( !to_folder.exists() ){
  to_folder.mkdirs()
}

Channel
  .fromPath("${from_folder}/*")
  .set{ files }

process copy {
  input:
    set file(m_file) from files

  exec:
    id = m_file.getBaseName()
    if( file("${to_folder}/${id}.txt").exists() ){
      state = "exists"
    }
    else{
      state = "execute"
    }

  script:
    if( state == "exists" )
      """
      echo exists
      """
    else
      """
      cp ${m_file} ${to_folder}
      """
}
