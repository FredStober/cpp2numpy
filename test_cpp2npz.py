#!/usr/bin/env python

import numpy

numpy.load('a.npz')
a = numpy.load('a.npz')

def test(name, expected):
	read = a[name]
	if numpy.array_equal(read, expected):
		print '%s ok' % name
	else:
		print '%s array contents not as expected: '
		print 'got: ', read, '; expected: ', expected

test('test0', range(1, 11))
test('test1', range(1, 11))

matrix = [[-1.0, 2.0, 5.8, 0.666], [2.7, 5.0, 2.78, 0.665], [8.6, 7.5, 3.2, 0.01]]
test('test2', matrix)
