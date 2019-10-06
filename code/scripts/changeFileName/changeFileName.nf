params.input = ""
params.pair = ""
params.output = ""

input_folder = file(params.input)
if( !input_folder.exists() ){
  error "No input folder: ${input_folder} folder."
}

pari_file = file(params.pair)
if( !pari_file.exists() ){
  error "No pari file: ${pari_file}."
}

if( params.output == ""){
  error "--output must be set."
}
else{
  output_folder = file(params.output)
  if ( !output_folder.exists() ){
    output_folder.mkdirs()
  }
}

Channel
  .fromPath(pari_file)
  .splitCsv(sep:'\t')
  .subscribe{ row ->
    org = file("${input_folder}/${row[0]}.txt")
    if ( !org.exists() ) {
      println "${org} is not exists."
    }
    else{
      org.copyTo("${output_folder}/${row[1]}.txt")
    }
  }
