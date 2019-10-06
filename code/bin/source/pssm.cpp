#include <fstream>
#include <sstream>
#include <cmath>
#include <iostream>
#include "term.h"
#include "pssm.h"
#include <stdlib.h>

PSSM::PSSM(const char *file_name)
{
	string AMINOACID_ORDER_PSSM = "ARNDCQEGHILKMFPSTWYV";
	int j, tmp, index;
	string str;
	fstream file;
	stringstream ss;
	float wei;
	char tmp_c;
	int len = 0;

	file.open(file_name, ios::in);
	while (!file.eof())
	{
		getline(file,str);
		ss.clear(); ss.str(str);

		if(ss >> tmp >> tmp_c) //prase line format:     1 M
	        	++len;
	}
	file.close();

	data.resize(len);
	file.open(file_name, ios::in);
	if(!file)
	{
		perror(file_name);
		exit(0);
	}
	getline(file, str); 	getline(file, str); 	getline(file, str);

	for(j = 0; j < len; j++)
	{
		getline(file, str);
		if((int)str.length() > 0)
		{
			str = str.substr(10);
			ss.clear(); ss.str(str);
			index = 0;
			while((ss >> tmp)&&((int)data[j].size() < 20))
			{
				wei = 1/(1+exp(-tmp));
				data[j].insert(make_pair(AMINOACID_ORDER_PSSM[index],wei));
				index++;
			}
		}
		if((int)data[j].size() != 20)
		{
		  	cout << "[ERROR] " << file_name << " " << j+1 << "-th position" << endl
			<< "PSSM feature size : "  << (int)data[j].size() << " != 20" << endl;
			exit(0);
		}
	}
	file.close();
	file.clear();
}

// draw number from normal random distribution
#ifndef PI
#define PI 3.141592653589793238462643
#endif

double normal(double x, double mean, double std)
{
	return (1/(std*sqrt(2.0*PI)))*exp((-0.5*(x-mean)*(x-mean))/(std*std));
}


void PSSM::normal_smooth()
{
	map<char, float>::iterator iter;
	double std = (double)data.size()/100;
	double wei;
	vector<map<char, float> > tmpData = data;
	bool wei_by_std = false;

	for(int i = 0; i < (double)data.size(); i++)
	{
		for(int j = 0; j < (double)data.size(); j++)
		{
			wei = wei_by_std?normal((double)j, (double)i, std):normal((double)j, (double)i, 5);
			for(iter = tmpData[j].begin(); iter != tmpData[j].end(); iter++)
				data[i][iter->first] += iter->second*wei;
		}
	}
}

void PSSM::window_smooth()
{
	map<char, float>::iterator iter;
	const int window_size = 5;
	vector<map<char, float> > tmpData = data;

	for(int i = 0; i < (int)data.size(); i++)
	{
		for(int j = -window_size; j <= window_size; j++)
		{
			if((i+j > 0)&&(i+j < (int)data.size()))
			{
				for(iter = tmpData[i+j].begin(); iter != tmpData[i+j].end(); iter++)
					data[i][iter->first] += iter->second;
			}
		}
	}
}

float PSSM::gap_dip_fre(gapped_dipeptide gapDip)
{
	float freSum = 0;

	// if(gapDip.gapLen+1 > (int)data.size())
	// {
	// 	cout << "ERROR: gapped didpeptide length > PSSM size" << endl;
	// 	return 0;
	// }

	for(int i = 0; i < (int)data.size()-gapDip.gapLen-1; i++)
		freSum += data[i][gapDip.head]*data[i+gapDip.gapLen+1][gapDip.tail];

	return freSum;
}
