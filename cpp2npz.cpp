#include <limits.h>
#include <stdlib.h>

#include <unistd.h>
#include <sys/wait.h>
#include <fcntl.h>

#include <errno.h>
#include <libgen.h>

#include <iostream>
#include <sstream>
#include <boost/filesystem.hpp>

#include "cpp2npz.h"

using namespace std;

IO_npz::IO_npz(const std::string &filename, Mode mode)
{
	boost::filesystem::path path(filename);
	std::string abspath = boost::filesystem::complete(path).string();
	zf = zipOpen(abspath.c_str(), 0);
}

void IO_npz::commit()
{
	if (zf)
	{
		zipClose(zf, NULL);
		zf = 0;
	}
}

std::string str(int i)
{
	std::ostringstream x;
	x << i;
	return x.str();
}

std::string get_shape(int ndims, int *shape)
{
	if (ndims == 1)
		return "(" + str(shape[0]) + ",)";
	std::string x = "(";
	for (int i = 0; i < ndims - 1; ++i)
		x += str(shape[i]) + ",";
	x += str(shape[ndims - 1]);
	return x + ")";
}

void IO_npz::add_entry(const std::string &name,
	const std::string desc, const std::string shape,
	const unsigned long size, const char *data)
{
	if (names.find(name) != names.end())
	{
		cerr << "Duplicate numpy entry: " << name << endl;
		throw;
	}
	zip_fileinfo zi;
	zi.internal_fa = zi.external_fa = 0;
	zi.tmz_date.tm_sec = zi.tmz_date.tm_min = zi.tmz_date.tm_hour =
	zi.tmz_date.tm_mday = zi.tmz_date.tm_mon = zi.tmz_date.tm_year = 0;
	zi.dosDate = 0;

	int err;
	err = zipOpenNewFileInZip3(zf, name.c_str(), &zi,
		NULL, 0, NULL, 0, NULL,
		Z_DEFLATED, Z_DEFAULT_COMPRESSION, 0,
		-MAX_WBITS, DEF_MEM_LEVEL, Z_DEFAULT_STRATEGY, 0, 0);

	// Basic numpy header
	static const unsigned char npy_magic[6] = {0x93, 'N', 'U', 'M', 'P', 'Y'};
	static const unsigned char npy_major = 1;
	static const unsigned char npy_minor = 0;

	// Build array description
	std::string array_info = "{";
	array_info += "'descr': '" + desc + "', ";
	array_info += "'fortran_order': False, ";
	array_info += "'shape': " + shape + ", }";
	unsigned short headlen = 0;
	while ((sizeof(npy_magic) + sizeof(npy_major) + sizeof(npy_minor) +
		sizeof(headlen) + array_info.size()) % 16 != 15)
		array_info += " ";
	array_info += "\n";
	headlen = array_info.size();

	// Write header
	err = zipWriteInFileInZip(zf, npy_magic, sizeof(npy_magic));
	err = zipWriteInFileInZip(zf, &npy_major, sizeof(npy_major));
	err = zipWriteInFileInZip(zf, &npy_minor, sizeof(npy_minor));
	err = zipWriteInFileInZip(zf, &headlen, sizeof(headlen));
	err = zipWriteInFileInZip(zf, array_info.c_str(), array_info.size());

	// Write data & close file
	err = zipWriteInFileInZip(zf, data, size);
	err = zipCloseFileInZip(zf);
	names.insert(name);
}

void IO_npz::add_entry(const std::string &name, const std::string desc,
	int ndims, int *shape, int type_size, const char *data)
{
	unsigned long rawsize = type_size;
	for (int i = 0; i < ndims; ++i)
		rawsize *= shape[i];
	add_entry(name, desc + str(type_size), get_shape(ndims, shape), rawsize, data);
}

void IO_npz::add_array(const std::string &name, int ndims, int *shape, double *data)
{
	add_entry(name, "<f", ndims, shape, sizeof(double), (const char *)data);
}

void IO_npz::add_array(const std::string &name, int ndims, int *shape, float *data)
{
	add_entry(name, "<f", ndims, shape, sizeof(float), (const char *)data);
}
