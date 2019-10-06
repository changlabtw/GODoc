params.type = ""
params.mode = ""
params.train_vec = ""
params.train_label = ""
params.test_vec = ""
params.vec_format = "t"
params.k = ""
params.threshold = ""
params.score_formula = "0"
params.output = "results"
params.chunkSize = 1

/*
 * Initialization
 */

 if( params.type == "" ){
   error "type must be setted"
 }

 if( params.mode == "" ){
   error "mode must be setted"
 }

 if( params.mode == "k" ){
   if ( params.k == "" ){
     error "In mode k, k must be setted"
   }
 }
 else if ( params.mode == "d" ){
   if ( params.threshold == "" ){
     error "In mode d, threshold must be setted"
   }
 }
 else {
   error "mode must be k or d"
 }

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
 * Run KNN and output score.txt
 */

process predict {

    output:
      file knn_res
      file vote_res

    script:
      if( params.mode == "k" ){
        """
        knn.py -train ${train_vec_file} -test ${test_vec_file} -f ${params.vec_format} -k ${params.k} -d True -o knn_res
        leafVote.py -i knn_res -l ${train_label_file} -s ${params.score_formula} -o vote_res
        """
      }
      else if( params.mode == "d"){
        """
        knn.py -train ${train_vec_file} -test ${test_vec_file} -f ${params.vec_format} -t ${params.threshold} -d True -o knn_res
        leafVote.py -i knn_res -l ${train_label_file} -s ${params.score_formula} -o vote_res
        """
      }

}

/*
 * Output files
 */

knn_res
  .subscribe{
    it.moveTo("${output_folder}/knn_res.tsv")
  }
vote_res
  .subscribe{
    it.moveTo("${output_folder}/${output_folder.getName()}.txt")
  }
