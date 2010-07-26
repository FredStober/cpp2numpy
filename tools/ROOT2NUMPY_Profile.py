#!/usr/bin/env python

import ROOT, numpy, sys
from ROOTutils import TProfileWrapper

def main(args):
	print "Processing %s" % args[0]
	file = ROOT.TFile(args[0])

	histo = TProfileWrapper(file.Get(args[1]))
	numpy.savez(args[1].split('/')[-1] + '.npz', x=histo.x(), xe=histo.xe(), y=histo.y(), ye=histo.ye())

if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))
