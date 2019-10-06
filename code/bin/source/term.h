#ifndef _TERM_H
#define _TERM_H

#include <vector>
#include <string>

using namespace std;

struct gapped_dipeptide
{
	char head;
	char tail;
	int gapLen;
};

class Term
{
public:
	Term();
	Term(int DISTANCE_THRESHOLD);
	Term(string filePath);
	void initial(int DISTANCE_THRESHOLD);
	void initial(string file);
	int size() const {return (int)term_vec.size();}
	gapped_dipeptide get_term(int i) const {return term_vec[i];}
private:
	vector<gapped_dipeptide> term_vec;
};

#endif /* _TERM_H */
