#!/usr/bin/env python

import ROOT, numpy, sys
from ROOTutils import TGraphWrapper

def main(args):
	print "Processing %s" % args[0]
	file = ROOT.TFile(args[0])

	for arg in args[1:]:
		histo = TGraphWrapper(file.Get(arg))
		numpy.savez(arg.split('/')[-1] + '.npz', x=histo.x(), xeh=histo.xeh(), xel=histo.xel(), y=histo.y(), yeh=histo.yeh(), yel=histo.yel())

if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))
