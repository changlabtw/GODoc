params.job = ""
params.output = "results/"
params.max = 1
pathpar = ["-i","-l","-train","-test"]

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
  .splitCsv(sep:'\t', header:["py","params"])
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
    for( i=0 ; i < pars.length ; i = i+2){
      if(pars[i] == "-o"){
        par_str = "${par_str}${pars[i]} ${output_folder}/${pars[i+1]} "
      }
      else if(pathpar.contains(pars[i])){
        par_str = "${par_str}${pars[i]} ${PWD}/${pars[i+1]} "
      }
      else{
        par_str = "${par_str}${pars[i]} ${pars[i+1]} "
      }
    }

  script:
    """
    python ${PWD}/${job} ${par_str}
    """

}

channel.subscribe{
  println it
}
