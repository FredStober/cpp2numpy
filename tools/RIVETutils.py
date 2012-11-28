import numpy

def readFlatFile(fn, hist):
	active = False
	title = None
	xaxis = None
	yaxis = None
	x = []
	x_err = []
	y = []
	y_err_l = []
	y_err_h = []
	for line in open(fn):
		if line.startswith('# BEGIN HISTOGRAM %s' % hist):
			active = True
		elif line.startswith('# END HISTOGRAM'):
			active = False
		elif line.startswith('#'):
			continue
		elif active and line.strip():
			line = line.strip()
			if line.startswith('AidaPath'):
				pass
			elif line.startswith('Title'):
				title = line.split('=', 1)[1]
			elif line.startswith('XLabel'):
				xaxis = line.split('=', 1)[1]
			elif line.startswith('YLabel'):
				yaxis = line.split('=', 1)[1]
			else:
## xlow  	xhigh   	val    	errminus	errplus
#1.800000e+01	2.100000e+01	3.885683e+06	6.575523e+04	6.575523e+04
				xlow, xhigh, val, errminus, errplus = map(float, line.split())
				x.append((xhigh + xlow) / 2.0)
				x_err.append((xhigh - xlow) / 2.0)
				y.append(val)
				y_err_l.append(errminus)
				y_err_h.append(errplus)

	return {'title': title, 'xlabel': xaxis, 'ylabel': yaxis,
		'x': numpy.array(x), 'xe': numpy.array(x_err),
		'y': numpy.array(y), 'ye': numpy.array([y_err_l, y_err_h])}
