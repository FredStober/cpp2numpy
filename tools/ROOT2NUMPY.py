#!/usr/bin/env python

import ROOT, numpy, sys
import ROOTutils

def main(args):
	if len(args) == 0:
		print "Usage: %s <ROOT FILE> <LIST OF HISTOGRAMS>" % sys.argv[0]
		sys.exit(1)
	print "Processing %s" % args[0]

	try:
		file = ROOT.TFile(args[0])
		plots = args[1:]
		if len(plots) == 0:
			# Read in all plots
			plots = []
			file.ls()

		for plot in plots:
			fn = args[1].split('/')[-1] + '.npz'
			obj = file.Get(plot.replace(".npz", ""))
			try:
				objclass = obj.ClassName()
			except:
				objclass = "Not found"

			if objclass.startswith("TH1"):
				histo = ROOTutils.TH1DWrapper(obj)
				numpy.savez(fn, x=histo.x(), xe=histo.xe(), y=histo.y(), ye=histo.ye())
			elif objclass.startswith("TH2"):
				histo = ROOTutils.TH2DWrapper(obj)
				numpy.savez(fn, x=histo.x_low(), y=histo.y_low(), z=histo.z())
			elif objclass.startswith("TProfile"):
				histo = ROOTutils.TProfileWrapper(obj)
				numpy.savez(fn, x=histo.x(), xe=histo.xe(), y=histo.y(), ye=histo.ye())
			elif objclass.startswith("TGraph"):
				histo = ROOTutils.TGraphWrapper(obj)
				numpy.savez(fn, x=histo.x(), xe=[histo.xel(), histo.xeh()],
					y=histo.y(), ye=[histo.yel(), histo.yeh()])
			else:
				print "Unsupported object: %s (%s)" % (plot, objclass)
	except:
		print "Error caused with arguments %s" % repr(args)
		raise

if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))
