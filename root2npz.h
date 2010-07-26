#include "cpp2npz.h"
#include <TH1D.h>
#include <TProfile.h>
#include <TH2D.h>
#include <TGraph.h>
#include <map>

/* root2npz.c -- ROOT IO for numpy files
   Version 0.01, Wed Mar 17 12:33:21 CET 2010

   Copyright (C) 2010 Fred Stober
*/

class TNumpy
{
public:
	enum IO_Scheme { IOS_SINGLE, IOS_POSTFIX, IOS_PREFIX };
	explicit TNumpy(const std::string &filename, const IO_Scheme s = IOS_SINGLE, const IO_npz::Mode m = IO_npz::OVERWRITE);

	void Add(TH1D *histo);
	void Add(TH2D *histo);
	void Add(TGraph *histo);

	void Write();

private:
	//do not allow copying or default construction:
	TNumpy(const IO_npz&);
	TNumpy();

	void Add(const std::map<std::string, std::pair<int, double*> > &data);
	std::string mapName(const std::string name, const TNamed *obj);
	IO_npz backend;
	IO_Scheme scheme;
};
