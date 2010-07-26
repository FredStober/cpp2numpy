#!/usr/bin/env python

import ROOT, numpy, sys
from ROOTutils import TH1DWrapper

def main(args):
	print "Processing %s" % args[0]
	file = ROOT.TFile(args[0])

	histo = TH1DWrapper(file.Get(args[1]))
	print histo.x()
	print histo.xe()
	print histo.y()
	print histo.ye()

	numpy.savez(args[1].split('/')[-1] + '.npz', x=histo.x(), xe=histo.xe(), y=histo.y(), ye=histo.ye())

if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))
