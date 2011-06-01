#!/usr/bin/env python

import ROOT, numpy, sys, os
import ROOTutils

def myGetName(x):
	objclass = x.GetClassName()
	if (objclass.startswith("TH") or objclass.startswith("TProfile") or objclass.startswith("TGraph")):
		#print x.GetName()
		return x.GetName()
	

def main(args):
	if len(args) == 0:
		print "Usage: %s <ROOT FILE> <LIST OF HISTOGRAMS>" % sys.argv[0]
		sys.exit(1)
	print "Processing %s" % args[0]

	try:
		file = ROOT.TFile(args[0])
		plots = args[1:]
		single = True
		if len(plots) == 0:
			# Read in all plots
			single = False
			plots = map(myGetName,list(file.GetListOfKeys()))
		x = {}
		xe = {}
		y = {}
		ye = {}

		for plot in plots:
			fn = plot.split('/')[-1] + '.npz'
			obj = file.Get(plot)
			try:
				objclass = obj.ClassName()
			except:
				objclass = "Not found"

			if objclass.startswith("TH1"):
				continue
				histo = ROOTutils.TH1DWrapper(obj)
				x[plot] = histo.x()
				xe[plot] =histo.xe()
				y[plot] = histo.y()
				ye[plot] = histo.ye()
			elif objclass.startswith("TH2"):
				histo = ROOTutils.TH2DWrapper(obj)
				x[plot] = histo.x_low()
				xe[plot] = histo.xe()
				y[plot] = histo.y_low()
				ye[plot] = histo.z()
				
			elif objclass.startswith("TProfile"):
				histo = ROOTutils.TProfileWrapper(obj)
				x[plot] = histo.x()
				xe[plot] = histo.xe()
				y[plot] = histo.y()
				ye[plot] = histo.ye()
			elif objclass.startswith("TGraph") or objclass.endswith('Graph'):
				histo = ROOTutils.TGraphWrapper(obj)
				x[plot] = histo.x()
				xe[plot] = [histo.xel(), histo.xeh()]
				y[plot] = histo.y()
				ye[plot] = [histo.yel(), histo.yeh()]
			else:
				print "Unsupported object: %s (%s)" % (plot, objclass)
			if single:
				numpy.savez(fn, x = x[plot], xe = xe[plot], y = y[plot], ye = ye[plot])

		if not single:
			rename = lambda (plot, content), ax: ("%s_%s" % (plot, ax), content)
			out = map(lambda c: rename(c, 'x'), x.items()) + \
			      map(lambda c: rename(c, 'y'), y.items()) + \
			      map(lambda c: rename(c, 'xe'), xe.items()) + \
			      map(lambda c: rename(c, 'ye'), ye.items())


			numpy.savez(os.path.basename(args[0])+'.npz', **dict(out))
			print "%s.npz" % args[0]
			print "saved all in one file"
				
	except:
		print "Error caused with arguments %s" % repr(args)
		raise

if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))
