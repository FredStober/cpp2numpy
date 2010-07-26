#!/usr/bin/env python

import ROOT, numpy, sys
from ROOTutils import TH1DWrapper

def main(args):
	print "Processing %s" % args[0]
	file = ROOT.TFile(args[0])

	rootHist = file.Get(args[1])
	binValues = map(float, args[2][1:].split(";"))
	if args[2][0] == 'X':
		axis = rootHist.GetXaxis()
		bin_a = axis.FindBin(binValues[0])
		bin_b = axis.FindBin(binValues[1])
		histo = TH1DWrapper(rootHist.ProjectionY("_proj", bin_a, bin_b, "e"))
	elif args[2][0] == 'Y':
		axis = rootHist.GetYaxis()
		bin_a = axis.FindBin(binValues[0])
		bin_b = axis.FindBin(binValues[1])
		histo = TH1DWrapper(rootHist.ProjectionX("_proj", bin_a, bin_b, "e"))
	else:
		return 0
	print axis.GetBinCenter(bin_a), binValues, bin_a, bin_b

	numpy.savez(args[1].split('/')[-1] + '.npz', x=histo.x(), xe=histo.xe(), y=histo.y(), ye=histo.ye())

if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))
