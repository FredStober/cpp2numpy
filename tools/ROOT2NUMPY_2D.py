#!/usr/bin/env python

import ROOT, numpy, sys
from ROOTutils import TH2DWrapper

def main(args):
	print "Processing %s" % args[0]
	file = ROOT.TFile(args[0])

	histo = TH2DWrapper(file.Get(args[1]))
	numpy.savez(args[1].split('/')[-1] + '.npz', x=histo.x_low(), y=histo.y_low(), z=histo.z())

if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))
