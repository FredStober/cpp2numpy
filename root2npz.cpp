#include "root2npz.h"
#include <iostream>
using namespace std;

TNumpy::TNumpy(const string &filename, const IO_Scheme s, const IO_npz::Mode m) :
	backend(filename, m), scheme(s)
{
}

void TNumpy::Add(const map<string, pair<int, double*> > &data)
{
	for (map<string, pair<int, double*> >::const_iterator it = data.begin(); it != data.end(); ++it)
		backend.add_array(it->first, vector<int>(1, it->second.first), it->second.second);
}

void TNumpy::Add(TH1D *histo)
{
	map<string, pair<int, double*> > tmp;
	TAxis *xax = histo->GetXaxis();

	vector<double> x(xax->GetNbins(), 0);
	for (int i = 1; i <= xax->GetNbins(); ++i)
		x[i-1] = xax->GetBinCenter(i);
	tmp[mapName("x", histo)] = make_pair(x.size(), &(x[0]));

	vector<double> xe(xax->GetNbins(), 0);
	for (int i = 1; i <= xax->GetNbins(); ++i)
		xe[i-1] = xax->GetBinWidth(i) / 2;
	tmp[mapName("xe", histo)] = make_pair(xe.size(), &(xe[0]));

	vector<double> y(xax->GetNbins(), 0);
	for (int i = 1; i <= xax->GetNbins(); ++i)
		y[i-1] = histo->GetBinContent(i);
	tmp[mapName("y", histo)] = make_pair(y.size(), &(y[0]));

	vector<double> ye(xax->GetNbins(), 0);
	for (int i = 1; i <= xax->GetNbins(); ++i)
		ye[i-1] = histo->GetBinError(i);
	tmp[mapName("ye", histo)] = make_pair(ye.size(), &(ye[0]));

	Add(tmp);
}

void TNumpy::Add(TH2D *histo)
{
	map<string, pair<int, double*> > tmp;
	TAxis *xax = histo->GetXaxis();
	TAxis *yax = histo->GetYaxis();

	vector<double> x(xax->GetNbins() + 1, 0);
	for (int i = 1; i <= xax->GetNbins(); ++i)
		x[i-1] = xax->GetBinLowEdge(i);
	x[xax->GetNbins()] = xax->GetBinUpEdge(xax->GetNbins());
	tmp[mapName("x", histo)] = make_pair(x.size(), &(x[0]));

	vector<double> y(yax->GetNbins() + 1, 0);
	for (int i = 1; i <= yax->GetNbins(); ++i)
		y[i-1] = yax->GetBinLowEdge(i);
	y[yax->GetNbins()] = yax->GetBinUpEdge(yax->GetNbins());
	tmp[mapName("y", histo)] = make_pair(y.size(), &(y[0]));

	Add(tmp);

	vector<double> z(xax->GetNbins() * yax->GetNbins(), 0);
	int bin = 0;
	for (int j = 1; j <= yax->GetNbins(); ++j)
		for (int i = 1; i <= xax->GetNbins(); ++i)
			z[bin++] = histo->GetBinContent(histo->GetBin(i, j));
	vector<int> shape(2, 0);
	shape[1] = xax->GetNbins();
	shape[0] = yax->GetNbins();
	backend.add_array(mapName("z", histo), shape, &(z[0]));
}

void TNumpy::Add(TGraph *histo)
{
	// NOT YET TESTED!
	return;
	const int N = histo->GetN();
	map<string, pair<int, double*> > tmp;

	tmp[mapName("x", histo)] = make_pair(N, histo->GetX());
	tmp[mapName("y", histo)] = make_pair(N, histo->GetY());
	Add(tmp);

	vector<int> shape(2, 0);
	shape[0] = 2;
	shape[1] = N;

	const double *exl = self.histo.GetEXlow()
	const double *exh = self.histo.GetEXhigh()
	vector<double> xe(2 * N);
	for (int i = 0; i < N; ++i)
		xe[i] = exl[i];
	for (int i = 0; i < N; ++i)
		xe[i + N] = exl[i];
	backend.add_array(mapName("xe", histo), shape, &(xe[0]));

	const double *eyl = self.histo.GetEYlow()
	const double *eyh = self.histo.GetEYhigh()
	vector<double> ye(2 * N);
	for (int i = 0; i < N; ++i)
		ye[i] = eyl[i];
	for (int i = 0; i < N; ++i)
		ye[i + N] = eyl[i];
	backend.add_array(mapName("ye", histo), shape, &(ye[0]));
)

void TNumpy::Write()
{
	backend.commit();
}

std::string TNumpy::mapName(const std::string name, const TNamed *obj)
{
	switch (scheme)
	{
		case IOS_PREFIX:
			return name + "_" + obj->GetName();
		case IOS_POSTFIX:
			return obj->GetName() + ("_" + name);
		default:
			return name;
	}
}
