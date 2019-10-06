#ifndef _PSSM_H
#define _PSSM_H

#include <vector>
#include <map>

class PSSM
{
public:
	PSSM(const char *file_name);
	void normal_smooth();
	void window_smooth();
	float gap_dip_fre(gapped_dipeptide gapDip);
private:
	vector<map<char, float> > data;
};

#endif /* _PSSM_H */
