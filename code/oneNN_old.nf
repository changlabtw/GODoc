params.train_vec = ""
params.train_label = ""
params.test_vec = ""
params.test_label = ""
params.vec_format = "c"
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

test_label_file = file(params.test_label)
if( !test_label_file.exists() ){
  error "No test_label_file file: ${test_label_file}."
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
      file oneNN_assign
      file res_measure

    script:
      """
      knn.py -train ${train_vec_file} -test ${test_vec_file} -f ${params.vec_format} -o knn_res
      oneNNLabel.py knn_res ${train_label_file} ${test_label_file} oneNN_assign
      pureMeasure.py oneNN_assign res_measure
      """
}

/*
 * Output files
 */

 knn_res
   .subscribe{
     it.moveTo("${output_folder}/oneNN_res.tsv")
   }
 oneNN_assign
   .subscribe{
     it.moveTo("${output_folder}/oneNN_assign.tsv")
   }
 res_measure
   .subscribe{
     it.moveTo("${output_folder}/res_measure")
   }
