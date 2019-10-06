params.query = ""
params.psiBlast = ""
params.output = "$PWD/stfpssm/"
params.h_d = 13
params.e_d = 5
params.c_d = 10
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

if ( params.query == "" ){
  error "--query should be set."
}

if ( params.psiBlast == "" ){
  error "--psiBlast should be set."
}

horizResult_folder = file(params.query)
if( !horizResult_folder.exists() ){
  error "No PSIPRED result folder: ${horizResult_folder}."
}

psiBlastResult_folder = file(params.psiBlast)
if( !psiBlastResult_folder.exists() ){
  error "No PSI-BLAST result folder: ${psiBlastResult_folder}."
}

stfpssm_folder = file(params.output)
if( !stfpssm_folder.exists() ){
  stfpssm_folder.mkdirs()
  all_stfpssm_folder = file(params.output + "all/")
  if( !all_stfpssm_folder.exists() ){
    all_stfpssm_folder.mkdirs()
  }
  helix_stfpssm_folder = file(params.output + "helix/")
  if( !helix_stfpssm_folder.exists() ){
    helix_stfpssm_folder.mkdirs()
  }
  sheet_stfpssm_folder = file(params.output + "sheet/")
  if( !sheet_stfpssm_folder.exists() ){
    sheet_stfpssm_folder.mkdirs()
  }
  coil_stfpssm_folder = file(params.output + "coil/")
  if( !coil_stfpssm_folder.exists() ){
    coil_stfpssm_folder.mkdirs()
  }
}

/*
 * Do tfpssm
 */

Channel
  .fromPath("${horizResult_folder}/*.horiz")
  .set { horizs }

process stfpssm {

  // maxForks 1

  input:
    set file(horiz) from horizs

  output:
    set id, state, file('m_stfpssm'), file('m_helix_stfpssm'), file('m_sheet_stfpssm'), file('m_coil_stfpssm') into m_stfpssms
    stdout channel

  exec:
    id = horiz.getBaseName()
    //check stfpssm exists
    if( file("${stfpssm_folder}/all/${id}.txt").exists() ){
      state = "exists"
    }
    else if( !file("${psiBlastResult_folder}/${id}.txt").exists() ){
      //check PSI-BLAST result exists
      state = "skip"
    }
    else{
      m_horiz = file("${horizResult_folder}/${id}.horiz")
      counta = 0
      m_horiz.eachLine{
        counta++
      }
      if( counta<=1 ){
        state = "skip"
      }
      else{
        pisblast = file("${psiBlastResult_folder}/${id}.txt")
        countb = 0
        pisblast.eachLine{
          countb++
        }
        if( countb<=1 ){
          state = "skip"
        }
        else{
          state = "execute"
        }
      }
    }
    // println state

    // //check stfpssm exists
    // if( file("${stfpssm_folder}/${id}.txt").exists() ){
    //   state = "exists"
    // }
    // else if( !haveResult("${horizResult_folder}/${id}.horiz") ){
    //   //check PSIPRED result has result
    //   state = "skip"
    // }
    // else if( !file("${psiBlastResult_folder}/${id}.txt").exists() ){
    //   //check PSI-BLAST result exists
    //   state = "skip"
    // }
    // else if( !haveResult("${psiBlastResult_folder}/${id}.txt") ){
    //   //check PSI-BLAST result has result
    //   state = "skip"
    // }
    // else{
    //   state = "execute"
    // }

  script:
    if( state == "exists" )
      """
      printf "exists" > m_stfpssm
      printf "exists" > m_helix_stfpssm
      printf "exists" > m_sheet_stfpssm
      printf "exists" > m_coil_stfpssm
      """
    else if( state == "skip" )
      """
      printf "skip" > m_stfpssm
      printf "skip" > m_helix_stfpssm
      printf "skip" > m_sheet_stfpssm
      printf "skip" > m_coil_stfpssm
      """
    else if( state == "execute" )
      """
      python $PWD/python/structure/parseStructure.py -i $horiz -o structure_str
      python $PWD/python/structure/slicePSSM.py -s structure_str -p ${psiBlastResult_folder}/${id}.txt -o sliced_folder
      mkdir tfpssms tfpssms/h tfpssms/e tfpssms/c
      $PWD/python/structure/stfpssm.sh ${params.h_d} ${params.e_d} ${params.c_d}
      python $PWD/python/structure/mergeVector.py -a tfpssms/h/ -b tfpssms/e/ -c tfpssms/c/ -o m_stfpssm -oa m_helix_stfpssm -ob m_sheet_stfpssm -oc m_coil_stfpssm
      """

}

m_stfpssms.subscribe{
  if ( it[1] == "exists" ){
    println "${it[0]}.txt already exists."
  }
  else if ( it[1] == "skip" ){
    println "${it[0]} doesn't have PSI-BLAST result or doesn't have PSIPRED result"
  }
  else{
    it[2].moveTo("${stfpssm_folder}/all/${it[0]}.txt")
    println "Save all stfpssm result to ${stfpssm_folder}/all/${it[0]}.txt"
    it[3].moveTo("${stfpssm_folder}/helix/${it[0]}.txt")
    println "Save helix stfpssm result to ${stfpssm_folder}/helix/${it[0]}.txt"
    it[4].moveTo("${stfpssm_folder}/sheet/${it[0]}.txt")
    println "Save sheet stfpssm result to ${stfpssm_folder}/sheet/${it[0]}.txt"
    it[5].moveTo("${stfpssm_folder}/coil/${it[0]}.txt")
    println "Save coil stfpssm result to ${stfpssm_folder}/coil/${it[0]}.txt"
  }
}

channel.subscribe{
  // println it
}
