# PPS

## Dependencies
1. PSI-BLAST
2. FactoMineR R package
2. Nextflow
3. Pandas Python package
4. Biopython Python package
5. [goatools](https://github.com/tanghaibao/goatools)
6. numpy 1.9.2+
7. scipy 0.13.0b1+
8. sklearn 0.17.1+

## nextflow.config
`params.db = "blast_db_path"`

## Nextflow Scripts
1. psiblast.nf
  * Goal: sequnece -> psiblast result
  * Usage:
    * nextflow psiblast.nf - -dataset small
    * nextflow psiblast.nf - -query seq.fasta - -output psiBlastResult
  * Note: result save as [sequence ID].txt. If no psiblast result, the content will only have the sequence, and the  ID will be logged at noresult.txt. The script will check the output exists or not, if output exists script will skip it to save time.
2. blastToTfpssm.nf
  * Goal: psiblast -> tfpssm
  * Usage:
    * nextflow blastToTfpssm.nf --query psiBlastResult/
    * nextflow blastToTfpssm.nf --query psiBlastResult/ --output results
3. tfpssm.nf
  * Goal: sequence -> psiblast -> tfpssm
  * Usage:
    * nextflow tfpssm.nf --dataset small
    * nextflow tfpssm.nf --query seq.fasta --output results
  * Note: psiblast result and tfpssm save as [sequence ID].txt in psiBlastResult and tfpssm folder. If no psiblast result, the psiblast result content will only have the sequence, and tfpssm will be nan…. The script will check the output exists or not, if output exists script will skip it to save time.
4. merge_tfpssm.nf
  * Goal: merge tfpssms to a model_tfpssm
  * Usage:
    * nextflow merge_tfpssm.nf --dataset test
    * nextflow merge_tfpssm.nf --tfpssm/ tfpssm --label function.tsv
5. train.nf
  * Goal: train PSLDoc2 model
  * Usage:
    * nextflow train.nf --dataset brief1000
    * nextflwo train.nf --tfpssm tfpssm/ --label function.tsv
  * Note:
6. pred.nf
  * Goal: use PSLDoc2 model to predict
  * Usage:
    * nextflow pred.nf --query seq.fasta --model model_tfpssm --modelLabel function.tsv
    * dataset and label are optional
  * Note: because predict target will need psiblast and tfpssm, so the script will check the psiblast result and tfpssm exists at dataset folder or not to save time.
