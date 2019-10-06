params.dataset = ""
params.query = "$PWD/data/${params.dataset}/seq.fasta"
params.output = "$PWD/data/${params.dataset}/psiPred/"
params.report = "noresult.txt" //append protein id if no psipred result
params.datadir = "$PWD/data/psipred_data"
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

if( (params.query == "$PWD/data/${params.dataset}/seq.fasta") != (params.output == "$PWD/data/${params.dataset}/psiPred/") ){
  error "--query and --output must be set same time."
}

query_file = file(params.query)
if( !query_file.exists() ){
  error "No sequence fasta file: ${query_file}."
}

psiPred_folder = file(params.output)
if( !psiPred_folder.exists() ){
  psiPred_folder.mkdirs()
}

datadir = file(params.datadir)
if( !datadir.exists() ){
  error "No data folder: ${datadir}."
}

report_file = file("${psiPred_folder}/${params.report}")
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
 * Execute a psipred job for each chunk for the provided sequences
 * If the psipred result already exists, the state will be exists
 * and nothing will be move to psiPred folder.
 * If the sequence does'n have a psipred result, the output text
 * file content will only have the sequence and the sequence ID will
 * be logged to noresult.txt at psiPred folder.
 */

process blast {

    input:
      set( id, file('seq.fa') ) from seq

    output:
      set( id, file('out'), state ) into psiPred_result
      stdout channel


    exec:
      if( file("${psiPred_folder}/${id}.horiz").exists() ){
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
        runpsipredplus seq.fa ${DB} ${datadir}
        [ -f seq.horiz ] && cat seq.horiz > out || cat seq.fa > out
        """
}

psiPred_result.subscribe{
  if ( it[2] == "exists" ){
    println "${it[0]}.horiz already exists."
  }
  else{
    if( haveResult(it[1]) ){
      println "Save PSI-BLAST result to ${psiPred_folder}/${it[0]}.horiz"
    }
    else{
      report_file.append("${it[0]}\n")
      println "${it[0]} doesn't have PSI-BLAST result."
    }
    it[1].moveTo("${psiPred_folder}/${it[0]}.horiz")
  }
}

channel.subscribe{
  println it
}
