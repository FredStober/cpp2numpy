#include "cpp2npz.h"
#include <iostream>

using namespace std;

int main()
{
	IO_npz n("a.npz");

	// Insert simple double vector
	vector<int> shape(1);
	shape[0] = 10;
	double data[10] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
	n.add_array("test0", shape, data);

	// again, under different name:
	n.add_array("test1", shape, data);

	// Insert simple double matrix
	double a[3][4] = {{-1.0, 2.0, 5.8, 0.666}, {2.7, 5.0, 2.78, 0.665}, {8.6, 7.5, 3.2, 0.01}};
	shape.resize(2);
	shape[0] = 3;
	shape[1] = 4;
	n.add_array("test2", shape, (double*)a);

	n.commit();
	return 0;
}
