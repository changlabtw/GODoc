#include <iostream>
#include <sstream>
#include <fstream>
#include "term.h"
#include <stdlib.h>

string AminoAcidStr = "ACDEFGHIKLMNPQRSTVWY";

Term::Term()
{
}

Term::Term(int DISTANCE_THRESHOLD)
{
	int i, j, k;
	gapped_dipeptide tmpGapDip;
	
	for(i = 0; i < (int)AminoAcidStr.length(); i++)
	{
		for(j = 0; j < (int)AminoAcidStr.length(); j++)
		{
			for(k = 0; k <= DISTANCE_THRESHOLD; k++)
			{
				tmpGapDip.head = *(AminoAcidStr.substr(i,1).c_str());
				tmpGapDip.tail = *(AminoAcidStr.substr(j,1).c_str());
				tmpGapDip.gapLen = k;
				term_vec.push_back(tmpGapDip);
			}
		}
	}
}

void Term::initial(string signature_file)
{
	gapped_dipeptide tmpGapDip;
	stringstream ss;
	string str_tmp;
	char head, tail;
	int distance;

	fstream file;
	file.open(signature_file.c_str());
	if(!file)
	{
		cout << "[ERROR] can not open signature file" << signature_file << endl;
		exit(1);
	}
	while(!file.eof())
	{
		getline(file, str_tmp);
		if((int)str_tmp.length() > 0)
		{
			ss.clear(); ss.str(str_tmp);
			ss >> head >> distance >> tail;
			tmpGapDip.head = head;
			tmpGapDip.tail = tail;
			tmpGapDip.gapLen = distance;
			term_vec.push_back(tmpGapDip);	
		}
	}
	file.close();
	cout << "Initial Gapped-Dipeptide by:\t" << signature_file << endl;
	cout << "# of Gapped-Dipeptides = " << (int)term_vec.size() << endl;
}

void Term::initial(int DISTANCE_THRESHOLD)
{
	int i, j, k;
	gapped_dipeptide tmpGapDip;
	
	for(i = 0; i < (int)AminoAcidStr.length(); i++)
	{
		for(j = 0; j < (int)AminoAcidStr.length(); j++)
		{
			for(k = 0; k <= DISTANCE_THRESHOLD; k++)
			{
				tmpGapDip.head = *(AminoAcidStr.substr(i,1).c_str());
				tmpGapDip.tail = *(AminoAcidStr.substr(j,1).c_str());
				tmpGapDip.gapLen = k;
				term_vec.push_back(tmpGapDip);
			}
		}
	}
}
