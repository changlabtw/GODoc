params.query = ""
params.hmmdb = ""
params.output = "$PWD/hmmPred_results/"
params.chunkSize = 1

/*
 * Initialization
 */

query_file = file(params.query)
if( !query_file.exists() ){
  error "No query file: ${query_file}."
}

hmmdb_file = file(params.hmmdb)
if( !hmmdb_file.exists() ){
  error "No hmm db: ${hmmdb_file}"
}
else{
  if( !file("${params.hmmdb}.h3i").exists() ){
    error "No hmm db: ${params.hmmdb}.h3i"
  }
  if( !file("${params.hmmdb}.h3f").exists() ){
    error "No hmm db: ${params.hmmdb}.h3f"
  }
  if( !file("${params.hmmdb}.h3p").exists() ){
    error "No hmm db: ${params.hmmdb}.h3p"
  }
}

output_folder = file(params.output)
if( !output_folder.exists() ){
  output_folder.mkdirs()
}

scanResult_folder = file("${params.output}/hmmscan_results/")
if( !scanResult_folder.exists() ){
  scanResult_folder.mkdirs()
}

/*
 * Split sequence FASTA file
 */

Channel
  .fromPath(query_file)
  .splitFasta( record: [id: true, seqString: true], by: params.chunkSize)
  .set { seq }

/*
 * Do hmmscan
 */

process hmmscan {

    input:
      set( id, file('seqStr') ) from seq

    output:
      set( id, file('out'), state ) into hmmscan_result

    exec:
      if( file("${scanResult_folder}/${id}.txt").exists() ){
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
        echo '>${id}' > seq.fa
        cat seqStr >> seq.fa
        hmmscan --tblout out ${hmmdb_file} seq.fa
        """
}

hmmscan_result.subscribe{
  if ( it[2] == "exists" ){
    println "${it[0]}.txt already exists."
  }
  else{
    println "Save hmmscan result to ${scanResult_folder}/${it[0]}.txt"
    it[1].moveTo("${scanResult_folder}/${it[0]}.txt")
  }
}
