#include <stdlib.h>
#include <string>
#include <fstream>
#include <iostream>
#include <iomanip>

#include "term.h"
#include "pssm.h"

bool fexists(string filename)
{
  ifstream ifile(filename.c_str());
  return ifile;
}


int main(int argc, char *argv[])
{
	// const int gappedDipeptides_dis=13;
	int i;
	float termWei, weiSum=0;
  string pssm_f; //input
  string tfpssm_f; //output
  int gappedDipeptides_dis = 13;
  if(argc == 3)
  {
    pssm_f  = argv[1]; //input
    tfpssm_f = argv[2]; //output
  }
  else if(argc == 4)
  {
    pssm_f  = argv[1]; //input
    tfpssm_f = argv[2]; //output
    gappedDipeptides_dis = atoi(argv[3]);
  }
	Term term(gappedDipeptides_dis);


	if(!fexists(tfpssm_f.c_str()))
	{

		cout << "process  = " << pssm_f << endl;
		cout << "generate = " << tfpssm_f << endl;

		float *saveVector = new float [(int)term.size()];

//open ouptut file
		fstream csvFile;
		csvFile.open(tfpssm_f.c_str(), ios::out);
		if(!csvFile)
		{
			perror(tfpssm_f.c_str());
			return 0;
		}

//check whether PSSM is a empty file
       std::ifstream file(pssm_f.c_str());
       bool empty_pssm = ((!file) || (file.peek() == std::ifstream::traits_type::eof()));
       if (file)
        file.close();

	   if(empty_pssm){
	   		cout << "[WARNNING] " << pssm_f << " is empty or does not exist " << endl;
   			for(i = 0; i < (int)term.size(); i++)
				csvFile << 0 << ",";
	   }
	   else{
			PSSM pssm(pssm_f.c_str());
			//pssm.normal_smooth();
			//pssm.window_smooth();

			for(i = 0; i < (int)term.size(); i++)
			{
				termWei = pssm.gap_dip_fre(term.get_term(i));
				saveVector[i] = termWei;
				weiSum += termWei;
			}
			//Normalization
			for(i = 0; i < (int)term.size(); i++)
					saveVector[i] = saveVector[i]/weiSum;
	//output TFPSSM to csv file
			for(i = 0; i < (int)term.size(); i++)
				csvFile << saveVector[i] << ",";
		}

		csvFile << endl;
		csvFile.close();

		delete [] saveVector;
	}else if(fexists(tfpssm_f)){
		cout << "tfpssm_file exist: " << tfpssm_f << endl;
	}
}
