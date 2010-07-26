#!/usr/bin/env python

import ROOT, numpy, sys
from ROOTutils import TH1DWrapper

def main(args):
	if (len(args) < 2):
		print "Nothing to do."
		return 0;

	print "Source File: %s" % args[0]
	file = ROOT.TFile(args[0])

	calc=0
	print "Error Calculation: copy"

	for arg in args[1:]:
		if (arg[0:2]=="--"):
			if ("--recalc-xy"==arg.lower()):
				print "Error Calculation: recalc-xy"
				calc=3
			elif ("--recalc-x"==arg.lower()):
				print "Error Calculation: recalc-x"
				calc=1
			elif ("--recalc-y"==arg.lower()):
				print "Error Calculation: recalc-y"
				calc=2
			elif ("--recalc-copy"==arg.lower()):
				print "Error Calculation: copy"
				calc=0
		else:
			print "Processing: %s" % arg
			histo = TH1DWrapper(file.Get(arg))
			if (calc==0):		# copy from source file
				numpy.savez(arg.split('/')[-1] + '.npz', x=histo.x(), xe=histo.xe(), y=histo.y(), ye=histo.ye())
			elif (calc==3):		# recalc XY
				numpy.savez(arg.split('/')[-1] + '.npz', x=histo.x(), xe=map(lambda x : numpy.sqrt(numpy.abs(x)), histo.x()), y=histo.y(), ye=map(lambda x : numpy.sqrt(numpy.abs(x)), histo.y()))
			elif (calc==1):		# recalc X
				numpy.savez(arg.split('/')[-1] + '.npz', x=histo.x(), xe=map(lambda x : numpy.sqrt(numpy.abs(x)), histo.x()), y=histo.y(), ye=histo.ye())
			elif (calc==2):		# recalc Y
				numpy.savez(arg.split('/')[-1] + '.npz', x=histo.x(), xe=histo.xe(), y=histo.y(), ye=map(lambda x : numpy.sqrt(numpy.abs(x)), histo.y()))

if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))
