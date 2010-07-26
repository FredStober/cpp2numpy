#include <string>
#include <vector>
#include <set>
#include "zip.h"

/* cpp2npz.c -- IO for numpy files
   Version 0.01, Wed Mar 17 12:33:21 CET 2010

   Copyright (C) 2010 Fred Stober, Jochen Ott

   zip library:
   Copyright (C) 1998-2005 Gilles Vollant, Rolf Kalbermatter
*/

class IO_npz
{
public:
	enum Mode { OVERWRITE = 0, APPEND = 2, MASK_OPENMODE = 3, LAZY = 4 };
	explicit IO_npz(const std::string &filename, Mode m = OVERWRITE);

	void add_entry(const std::string &name, const std::string desc,
		const std::string shape, const unsigned long size, const char *data);

	void add_entry(const std::string &name, const std::string desc,
		int ndims, int *shape, int type_size, const char *data);

	// add an array with the given name. ndims is the number of dimensions, i.e., number
	// of entries in the array shape. data is a pointer to the data to be saved.
	// It has to have
	//    shape[0] * shape[1] * ... * shape[ndims-1]
	// entries and has to have flat, C/C++-array-like layout, i.e., in the 2D case,
	//    array[i][j]
	// is located at data[i * shape[1] + j], where 0 <= i < shape[0] and 0 <= j < shape[1].
	//
	// A. "raw" routines with pointers.
	void add_array(const std::string &name, int ndims, int* shape, double *data);
	void add_array(const std::string &name, int ndims, int* shape, float *data);

	// B. some C++
	void add_array(const std::string &name, std::vector<int> shape, double *data)
	{
		add_array(name, (int)shape.size(), &(shape[0]), data);
	}

	void add_array(const std::string &name, std::vector<int> shape, float *data)
	{
		add_array(name, (int)shape.size(), &(shape[0]), data);
	}

	// C. more C++ for the simple case (i.e. for 1-dimensional arrays):
	void add_array(const std::string &name, std::vector<float> data)
	{
		int size = (int)data.size();
		add_array(name, 1, &size, &(data[0]));
	}

	void add_array(const std::string &name, std::vector<double> data)
	{
		int size = (int)data.size();
		add_array(name, 1, &size, &(data[0]));
	}

	void commit();

private:
	//do not allow copying or default construction:
	IO_npz(const IO_npz&);
	IO_npz();

	std::set<std::string> names;
	zipFile zf;
};
