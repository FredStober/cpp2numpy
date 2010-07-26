#!/usr/bin/env python

import numpy

def check(a,b,v):
	print a[v]
	print b[v]
	print a[v] == b[v]
	print

print "="*40
a = numpy.load('TEST_th1d.lib.npz')
b = numpy.load('TEST_th1d.npz')
check(a,b,'x')
check(a,b,'xe')
check(a,b,'y')
check(a,b,'ye')

print "="*40
a = numpy.load('TEST_th2d.lib.npz')
b = numpy.load('TEST_th2d.npz')
check(a,b,'x')
check(a,b,'y')
check(a,b,'z')

print "="*40
a = numpy.load('TEST_tprofile.lib.npz')
b = numpy.load('TEST_tprofile.npz')
check(a,b,'x')
check(a,b,'xe')
check(a,b,'y')
check(a,b,'ye')
