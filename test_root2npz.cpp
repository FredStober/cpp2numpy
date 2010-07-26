#include "root2npz.h"
#include <iostream>
#include <TFile.h>

using namespace std;

int main()
{
	TFile output("TEST.root", "RECREATE");
	int bin;

	//////////////////////////////////////////

	TNumpy npz("TEST_th1d.lib.npz");
	double xbins[5] = { -2, -0.5, 3, 6, 7 };
	TH1D plot_th1d("TEST_th1d", "TEST", 4, xbins);

	bin = plot_th1d.FindBin(-1);
	plot_th1d.SetBinContent(bin, 10);
	plot_th1d.SetBinError(bin, 2);

	bin = plot_th1d.FindBin(0);
	plot_th1d.SetBinContent(bin, 5);
	plot_th1d.SetBinError(bin, 1);

	bin = plot_th1d.FindBin(5);
	plot_th1d.SetBinContent(bin, 1);
	plot_th1d.SetBinError(bin, 0.5);

	plot_th1d.Write();
	npz.Add(&plot_th1d);
	npz.Write();

	//////////////////////////////////////////

	TNumpy npz_profile("TEST_tprofile.lib.npz");
	TProfile plot_tprofile("TEST_tprofile", "TEST", 5, 0, 10, "s");

	plot_tprofile.Fill(1, 1, 2);
	plot_tprofile.Fill(2, 3, 1);
	plot_tprofile.Fill(2, 3, 1);
	plot_tprofile.Fill(6, 2, 1);
	plot_tprofile.Fill(6, 4, 1);

	plot_tprofile.Write();
	npz_profile.Add(&plot_tprofile);
	npz_profile.Write();

	//////////////////////////////////////////

	TNumpy npz_th2d("TEST_th2d.lib.npz");
	double ybins[4] = { -1, 0, 2, 5 };
	TH2D plot_th2d("TEST_th2d", "TEST", 4, xbins, 3, ybins);

	bin = plot_th2d.FindBin(-1, -0.5);
	plot_th2d.SetBinContent(bin, 10);
	bin = plot_th2d.FindBin(-1, 0.5);
	plot_th2d.SetBinContent(bin, 6);
	bin = plot_th2d.FindBin(-1, 3);
	plot_th2d.SetBinContent(bin, 2);

	bin = plot_th2d.FindBin(0, -0.25);
	plot_th2d.SetBinContent(bin, 5);
	bin = plot_th2d.FindBin(0, 4);
	plot_th2d.SetBinContent(bin, 3);

	bin = plot_th2d.FindBin(5, 1);
	plot_th2d.SetBinContent(bin, 2);
	bin = plot_th2d.FindBin(5, 2);
	plot_th2d.SetBinContent(bin, 1);

	bin = plot_th2d.FindBin(6.5, -0.5);
	plot_th2d.SetBinContent(bin, 1);
	bin = plot_th2d.FindBin(6.5, 3);
	plot_th2d.SetBinContent(bin, -1);

	plot_th2d.Write();
	npz_th2d.Add(&plot_th2d);
	npz_th2d.Write();

	return 0;
}
