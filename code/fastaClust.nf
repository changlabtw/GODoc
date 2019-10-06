params.input = ""
params.output = "$PWD/fastaClust_results/"
params.nr = "$PWD/fastaClust_nr/"
params.chunkSize = 1
params.identities = 0.5

/*
 * Initialization
 */

fasta_folder = file(params.input)
if( !fasta_folder.exists() ){
  error "No fasta folder: ${fasta_folder}."
}

output_folder = file(params.output)
if( !output_folder.exists() ){
  output_folder.mkdirs()
}

nr_folder = file(params.nr)
if( !nr_folder.exists() ){
  nr_folder.mkdirs()
}

/*
 * Do hmmalign and hmmbuild
 */

Channel
  .fromPath("${fasta_folder}/*.fasta")
  .filter{
    it.text.length() - it.text.replace('>','').length() > 1
  }
  .set { fastas }

process cluster_fast {

  input:
    set file(fasta) from fastas

  output:
    stdout channel

  exec:
    id = fasta.getBaseName()

  script:
    """
    usearch -cluster_fast ${fasta} -sort length -id ${params.identities} -centroids ${nr_folder}/${id}_nr.fasta -clusters ${output_folder}/${id}_
    """
}
