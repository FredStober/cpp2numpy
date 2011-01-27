import numpy, math
import ROOT

class TH1DWrapper(object):
	def __init__(self, th1d):
		self.histo = th1d

	# Return lower x bounds
	def x_low(self):
		if not hasattr(self, "cache_x_low"):
			xaxis = self.histo.GetXaxis()
			self.cache_x_low = numpy.zeros(xaxis.GetNbins() + 1, dtype = numpy.double)
			xaxis.GetLowEdge(self.cache_x_low)
			self.cache_x_low[-1] = xaxis.GetBinUpEdge(xaxis.GetNbins())
		return self.cache_x_low

	# Return center x bounds (without over/underflow bin by default)
	def x(self, limits = False):
		if not hasattr(self, "cache_x"):
			xaxis = self.histo.GetXaxis()
			self.cache_x = numpy.zeros(xaxis.GetNbins() + 2, dtype = numpy.double)
			xaxis.GetCenter(self.cache_x[1:-1])
			self.cache_x[0] = xaxis.GetBinLowEdge(1)
			self.cache_x[-1] = xaxis.GetBinUpEdge(xaxis.GetNbins())
		if limits:
			return self.cache_x
		else:
			return self.cache_x[1:-1]

	# Return x error
	def xe(self):
		if not hasattr(self, "cache_xe"):
			self.cache_xe = map(lambda (low, c): c - low, zip(self.x_low()[:-1], self.x()))
		return self.cache_xe

	# Return y
	def y(self, limits = False, cont = True):
		if not hasattr(self, "cache_y"):
			xaxis = self.histo.GetXaxis()
			self.cache_y = numpy.zeros(xaxis.GetNbins() + 2)
			for i in range(self.histo.GetSize()):
				self.cache_y[i]=self.histo.GetArray()[i]
			numpy.ndarray(self.histo.GetSize(), buffer = self.histo.GetArray())
			self.cache_y_uflow = self.cache_y[0]
			self.cache_y_oflow = self.cache_y[-1]
		if cont:
			self.cache_y[0] = self.cache_y[1]
			self.cache_y[-1] = self.cache_y[-2]
		else:
			self.cache_y[0] = self.cache_y_uflow
			self.cache_y[-1] = self.cache_y_oflow
		if limits:
			return self.cache_y
		else:
			return self.cache_y[1:-1]

	# Return y sum of weights
	def ys2(self):
		if not hasattr(self, "cache_ys2"):
			array = self.histo.GetSumw2()
			self.cache_ys2 = numpy.ndarray(array.GetSize(), dtype = numpy.double, buffer = array.GetArray())
		return self.cache_ys2

	# Return y error
	def ye(self):
		if not hasattr(self, "cache_ye"):
			xaxis = self.histo.GetXaxis()
			self.cache_ye = numpy.zeros(xaxis.GetNbins() + 2)
			for i in range(self.histo.GetSize()):
				self.cache_ye[i]=self.histo.GetBinError(i)
			self.cache_ye_uflow = self.cache_ye[0]
			self.cache_ye_oflow = self.cache_ye[-1]
		return self.cache_ye[1:-1]


class TH2DWrapper(object):
	def __init__(self, th2d):
		self.histo = th2d

	# Return lower x bounds
	def x_low(self):
		if not hasattr(self, "cache_x_low"):
			xaxis = self.histo.GetXaxis()
			self.cache_x_low = numpy.zeros(xaxis.GetNbins() + 1, dtype = numpy.double)
			xaxis.GetLowEdge(self.cache_x_low)
			self.cache_x_low[-1] = xaxis.GetBinUpEdge(xaxis.GetNbins())
		return self.cache_x_low
	
	def x(self):
		if not hasattr(self, "cache_x"):
			xaxis = self.histo.GetXaxis()
			self.cache_x = numpy.zeros(xaxis.GetNbins(), dtype = numpy.double)
			xaxis.GetCenter(self.cache_x)
			#self.cache_x_low[-1] = xaxis.GetBinUpEdge(xaxis.GetNbins())
		return self.cache_x

	# Return x error
	def xe(self):
		if not hasattr(self, "cache_xe"):
			self.cache_xe = map(lambda (low, c): c - low, zip(self.x_low()[:-1], self.x()))
		return self.cache_xe	
	
	# Return lower y bounds
	def y_low(self):
		if not hasattr(self, "cache_y_low"):
			yaxis = self.histo.GetYaxis()
			self.cache_y_low = numpy.zeros(yaxis.GetNbins() + 1, dtype = numpy.double)
			yaxis.GetLowEdge(self.cache_y_low)
			self.cache_y_low[-1] = yaxis.GetBinUpEdge(yaxis.GetNbins())
		return self.cache_y_low

	def y(self):
		if not hasattr(self, "cache_y"):
			yaxis = self.histo.GetYaxis()
			#print yaxis.GetNbins(), " yaxis.GetNbins() yaxis.GetNbins() yaxis.GetNbins() yaxis.GetNbins() yaxis.GetNbins()"
			self.cache_y = numpy.zeros(yaxis.GetNbins(), dtype = numpy.double)
			yaxis.GetCenter(self.cache_y)
		return self.cache_y

	# Return y error
	def ye(self):
		if not hasattr(self, "cache_ye"):
			self.cache_ye = map(lambda (low, c): c - low, zip(self.y_low()[:-1], self.y()))
		return self.cache_ye	

	# Return z
	def z(self, limits = False):
		if not hasattr(self, "cache_z"):
			self.cache_z = numpy.ndarray(self.histo.GetSize(), dtype = numpy.double, buffer = self.histo.GetArray())
			self.cache_z_shaped = self.cache_z.reshape((len(self.y_low()) + 1, len(self.x_low()) + 1))
		if limits:
			return self.cache_z_shaped
		else:
			return self.cache_z_shaped[1:-1,1:-1]


class TProfileWrapper(TH1DWrapper):
	def __init__(self, th1d):
		TH1DWrapper.__init__(self, th1d)

	# Return y
	def y(self, limits = False, cont = True):
		if not hasattr(self, "cache_y"):
			xaxis = self.histo.GetXaxis()
			self.cache_y = numpy.zeros(xaxis.GetNbins() + 2)
			for i in range(self.histo.GetSize()):
				self.cache_y[i]=self.histo.GetBinContent(i)
			numpy.ndarray(self.histo.GetSize(), buffer = self.histo.GetArray())
			self.cache_y_uflow = self.cache_y[0]
			self.cache_y_oflow = self.cache_y[-1]
		if cont:
			self.cache_y[0] = self.cache_y[1]
			self.cache_y[-1] = self.cache_y[-2]
		else:
			self.cache_y[0] = self.cache_y_uflow
			self.cache_y[-1] = self.cache_y_oflow
		if limits:
			return self.cache_y
		else:
			return self.cache_y[1:-1]

	# Return y error
	def ye(self):
		if not hasattr(self, "cache_ye"):
			xaxis = self.histo.GetXaxis()
			self.cache_ye = numpy.zeros(xaxis.GetNbins() + 2)
			for i in range(self.histo.GetSize()):
				self.cache_ye[i]=self.histo.GetBinError(i)
			self.cache_ye_uflow = self.cache_ye[0]
			self.cache_ye_oflow = self.cache_ye[-1]
		return self.cache_ye[1:-1]

	#return x
	def x(self, limits = False):
		if not hasattr(self, "cache_x"):
			xaxis = self.histo.GetXaxis()
			self.cache_x = numpy.zeros(xaxis.GetNbins() + 2, dtype = numpy.double)
			xaxis.GetCenter(self.cache_x[1:-1])
			self.cache_x[0] = xaxis.GetBinLowEdge(1)
			self.cache_x[-1] = xaxis.GetBinUpEdge(xaxis.GetNbins())
		if limits:
			return self.cache_x
		else:
			return self.cache_x[1:-1]

	# Return x error
	def xe(self):
		if not hasattr(self, "cache_xe"):
			self.cache_xe = map(lambda (low, c): c - low, zip(self.x_low()[:-1], self.x()))
		return self.cache_xe


class TGraphWrapper():
	def __init__(self, th1d):
		self.histo = th1d

	# Return x
	def x(self):
		print self.histo
		if not hasattr(self, "cache_x"):
			self.cache_x = numpy.ndarray(self.histo.GetN(), dtype = numpy.double, buffer = self.histo.GetX())
		return self.cache_x

	# Return y
	def y(self):
		if not hasattr(self, "cache_y"):
			self.cache_y = numpy.ndarray(self.histo.GetN(), dtype = numpy.double, buffer = self.histo.GetY())
		return self.cache_y

	# Return xeh
	def xeh(self):
		if not hasattr(self, "cache_xeh"):
			self.cache_xeh = numpy.ndarray(self.histo.GetN(), dtype = numpy.double, buffer = self.histo.GetEXhigh())
		return self.cache_xeh

	# Return xel
	def xel(self):
		if not hasattr(self, "cache_xel"):
			self.cache_xel = numpy.ndarray(self.histo.GetN(), dtype = numpy.double, buffer = self.histo.GetEXlow())
		return self.cache_xel

	# Return yeh
	def yeh(self):
		if not hasattr(self, "cache_yeh"):
			self.cache_yeh = numpy.ndarray(self.histo.GetN(), dtype = numpy.double, buffer = self.histo.GetEYhigh())
		return self.cache_yeh

	# Return yel
	def yel(self):
		if not hasattr(self, "cache_yel"):
			self.cache_yel = numpy.ndarray(self.histo.GetN(), dtype = numpy.double, buffer = self.histo.GetEYlow())
		return self.cache_yel
