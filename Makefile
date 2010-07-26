CXX      = g++
CXXFLAGS = -O2 -Wall -fPIC $(shell ${ROOTSYS}/bin/root-config --cflags)

LD       = g++
LDFLAGS  = -O2 $(SYSLIBS) -L. $(shell ${ROOTSYS}/bin/root-config --libs)
LDFLAGS += -lz -lboost_filesystem -lboost_system

LIBFILES = root2npz.o cpp2npz.o zip.o ioapi.o
all: libroot2npz.so libroot2npz.a test_root2npz.bin

%.so: $(LIBFILES)
	$(LD) -shared $(LDFLAGS) -o $@ $^

%.a: $(LIBFILES)
	ar rcs $@ $^

%.o: %.cpp %.h
	$(CXX) $(CXXFLAGS) -c -o $@ $<

%.o: %.c %.h
	$(CC) $(CXXFLAGS) -DNOCRYPT -DNOUNCRYPT -c -o $@ $<

%.bin: %.o
	$(LD) $(LDFLAGS) -lroot2npz -o $@ $^

clean:
	@rm -f *.o *.so *.bin
