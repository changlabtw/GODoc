blast_cmd="psiblast -matrix BLOSUM80 -evalue 1e-5 -gapopen 9 -gapextend 2 -threshold 999 -seg yes -soft_masking true -num_iterations 3"

//params.db = ""  set db at nextflow.config
params.dataset = ""
params.query = "$PWD/data/${params.dataset}/seq.fasta"
params.output = "$PWD/data/${params.dataset}/psiBlastResult/"
params.report = "noresult.txt" //append protein id if no PSI-BLAST result
params.chunkSize = 1

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

if ( params.query == "$PWD/data/${params.dataset}/seq.fasta"){
  dataset_folder = file("$PWD/data/${params.dataset}")
  if( !dataset_folder.exists() ){
    error "No dataset: ${params.dataset} folder at $PWD/data/."
  }
}

if( (params.query == "$PWD/data/${params.dataset}/seq.fasta") != (params.output == "$PWD/data/${params.dataset}/psiBlastResult/") ){
  error "--query and --output must be set same time."
}

query_file = file(params.query)
if( !query_file.exists() ){
  error "No sequence fasta file: ${query_file}."
}

psiBlastResult_folder = file(params.output)
if( !psiBlastResult_folder.exists() ){
  psiBlastResult_folder.mkdirs()
}

report_file = file("${psiBlastResult_folder}/${params.report}")
if( !report_file.exists() ){
  report_file.append('')
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
 * and nothing will be move to psiBlastResult folder.
 * If the sequence does'n have a PSI-BLAST result, the output text
 * file content will only have the sequence and the sequence ID will
 * be logged to noresult.txt at psiBlastResult folder.
 */

process blast {

    input:
      set( id, file('seq.fa') ) from seq

    output:
      set( id, file('out'), state ) into blast_result

    script:
      if( file("${psiBlastResult_folder}/${id}.txt").exists() ){
        state = "exists"
      }
      else{
        state = "execute"
      }
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

blast_result.subscribe{
  if ( it[2] == "exists" ){
    println "${it[0]}.txt already exists."
  }
  else{
    if( haveResult(it[1]) ){
      println "Save PSI-BLAST result to ${psiBlastResult_folder}/${it[0]}.txt"
    }
    else{
      report_file.append("${it[0]}\n")
      println "${it[0]} doesn't have PSI-BLAST result."
    }
    it[1].moveTo("${psiBlastResult_folder}/${it[0]}.txt")
  }
}
