#ifndef _PROTEIN_H
#define _PROTEIN_H

#include <string>
#include <vector>
#include <ostream>

#include <gsl/gsl_matrix.h>
#include <gsl/gsl_blas.h>
#include <gsl/gsl_math.h>
#include <sys/stat.h>

bool fexist(const char *filename);

using namespace std;

struct PRE_ELEMENT
{
	string pre_label;
	vector<float> confidence;
};

class Protein
{
public:
	Protein();
	Protein(string name, string seq, vector<string> site);
	~Protein();
	void gen_PSSM(const char *pssm_dic_path, const struct PSLDoc_PARAMETER *param) const;
	void gen_TFPSSM(const char *pssm_dic_path, Term term, const struct PSLDoc_PARAMETER *param) const;
	void construct_fea_vec(const char *tfpssm_dic);
	void construct_fea_vec(const gsl_vector *gsl_vec);
	void show_fea(fstream& out) const;
	void show_site(fstream& out) const;
	void show_pred(fstream& out) const;
	void show_probability(fstream& out) const;
	void set_pred(Protein pro);
	int pred_correct() const;
	vector<float> get_fea_vec(){return fea_vec;};
	vector<string> get_site_vec() const {return site_vec;};
	int fea_size() const {return (int)fea_vec.size();};
	float get_fea(int i) const{return fea_vec[i];};
	string get_name() const {return name;};
	void push_pre(PRE_ELEMENT pre){pre_vec.push_back(pre);};
	
private:
	string name;
	string seq;
	vector<string> site_vec;
	vector<PRE_ELEMENT> pre_vec;
	vector<float> fea_vec;
};
#endif /* _PROTEIN_H */
