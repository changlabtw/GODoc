params.job = ""
params.output = "results/"
params.max = 1
pathpar = ["query","model","modelLabel","label","dataset","tfpssm","from","to","train_vec","train_label","test_vec","test_label","stfpssm"]

output_folder = file("${params.output}")
if( !output_folder.exists() ){
  output_folder.mkdirs()
}

job_file = file(params.job)
if( !job_file.exists() ){
  error "No job file: ${job_file}"
}

Channel
  .fromPath(job_file)
  .splitCsv(sep:'\t', header:["nf","params"])
  .set { jobs }

process DoJob {

  maxForks params.max

  input:
    set job, pars from jobs

  output:
    stdout channel

  exec:
    par_str = ""
    pars = pars.split(',')
    if( pars.length%2!=0 ){
      error "Params pairs are not matching."
    }
    for( i=0 ; i < pars.length ; i = i+2){
      if(pars[i] == "output"){
        par_str = "${par_str}--${pars[i]} ${output_folder}/${pars[i+1]} "
      }
      else if(pathpar.contains(pars[i])){
        par_str = "${par_str}--${pars[i]} ${PWD}/${pars[i+1]} "
      }
      else{
        par_str = "${par_str}--${pars[i]} ${pars[i+1]} "
      }
    }

  script:
    """
    nextflow ${PWD}/${job} ${par_str}
    """

}

channel.subscribe{
  println it
}
