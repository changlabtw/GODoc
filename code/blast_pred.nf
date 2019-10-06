blast_cmd='blastp -outfmt "6 qseqid sseqid evalue length pident nident"'

params.query = ""
params.train = ""
params.output = "$PWD/blast_pred_result/"
params.my_matlab_path = "$PWD/cafa2_eval/myscript"
params.matlab_path = "$PWD/cafa2_eval/matlab"
params.cat = "CCO"
params.ont_db_path = "$PWD/cafa2_eval/ontology/go_20130615-termdb.obo"
params.trian_oa_file = "$PWD/cafa2_eval/benchmark/groundtruth/propagated_CCO.txt" //Target protein labels
params.test_oa_file = "" //Training protein labels
params.benchmark = "$PWD/cafa2_eval/benchmark/lists/cco_all_type1.txt" //Target protein ID
params.chunkSize = 1

/*
 * Initialization
 */

query_file = file(params.query)
if( !query_file.exists() ){
  error "No query sequence fasta file: ${query_file}."
}

train_file = file(params.train)
if( !train_file.exists() ){
  error "No train sequence fasta file: ${train_file}."
}

output_folder = file(params.output)
if ( !output_folder.exists() ){
  output_folder.mkdirs()
}

/*
 * Run blastp
 */

process blastp_pred{
  input:
    file query_file
    file train_file

  output:
    file train_db
    file blastp_out
    file fmax
    file prcurve

  script:
    """
    mkdir train_db
    makeblastdb -in $train_file -dbtype prot -out train_db/train_db
    $blast_cmd -db train_db/train_db -query $query_file -out blastp_out
    python $PWD/python/fasta/ID.py -f $query_file -o target_file
    matlab -nodisplay -r \"addpath('${params.my_matlab_path}');\
                          blast_pred('${params.matlab_path}',\
                          '${params.cat}','${params.ont_db_path}',\
                          '${params.test_oa_file}','${params.train_oa_file}'\
                          ,'blastp_out','target_file',\
                          '${params.benchmark}','./');quit;\"
    mv fmax.txt fmax
    mv prcurve.csv prcurve
    """
}

/*
 * Output results
 */

train_db.subscribe{
  it.moveTo(output_folder)
}
blastp_out.subscribe{
  it.moveTo(output_folder)
}
fmax.subscribe{
  it.moveTo("${output_folder}/fmax.txt")
}
prcurve.subscribe{
  it.moveTo("${output_folder}/prcurve.csv")
}
