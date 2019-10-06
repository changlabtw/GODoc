params.train_vec = ""
params.train_label = ""
params.test_vec = ""
params.vec_format = "c"
params.my_matlab_path = "$PWD/cafa2_eval/myscript"
params.matlab_path = "$PWD/cafa2_eval/matlab"
params.cat = "CCO"
params.ont_db_path = "$PWD/cafa2_eval/ontology/go_20130615-termdb.obo"
params.oa_file = "$PWD/cafa2_eval/benchmark/groundtruth/propagated_CCO.txt" //Target protein labels
params.benchmark = "$PWD/cafa2_eval/benchmark/lists/cco_all_type1.txt" //Target protein ID
params.output = "results"
params.chunkSize = 1

/*
 * Initialization
 */

train_vec_file = file(params.train_vec)
if( !train_vec_file.exists() ){
  error "No train_vec file: ${train_vec_file}."
}

train_label_file = file(params.train_label)
if( !train_label_file.exists() ){
  error "No train_label_file file: ${train_label_file}."
}

test_vec_file = file(params.test_vec)
if( !test_vec_file.exists() ){
  error "No test_vec file: ${test_vec_file}."
}

output_folder = file(params.output)
if( !output_folder.exists() ){
  output_folder.mkdirs()
}

/*
 * Run 1NN and assgin predict labels
 */

process predict {

    output:
      file knn_res
      file leaf_score
      file fmax
      file prcurve
      stdout channel

    // seq_eval(matlab_path, cat, ont_db_path, oa_file, pred_file, benchmark_file, output_folder)
    script:
      """
      knn.py -train ${train_vec_file} -test ${test_vec_file} -f ${params.vec_format} -o knn_res
      1NN.py -i knn_res -l ${train_label_file} -o leaf_score
      matlab -nodisplay -r \"addpath('${params.my_matlab_path}');\
                            seq_eval('${params.matlab_path}',\
                            '${params.cat}','${params.ont_db_path}',\
                            '${params.oa_file}','leaf_score',\
                            '${params.benchmark}','./');quit;\"
      mv fmax.txt fmax
      mv prcurve.csv prcurve
      """
}

/*
 * Output files
 */

knn_res.subscribe{
  it.moveTo("${output_folder}/oneNN_res.tsv")
}
leaf_score.subscribe{
  it.moveTo("${output_folder}/leaf_score.txt")
}
fmax.subscribe{
  it.moveTo("${output_folder}/fmax.txt")
}
prcurve.subscribe{
  it.moveTo("${output_folder}/prcurve.txt")
}
channel.subscribe{
  println it
}
