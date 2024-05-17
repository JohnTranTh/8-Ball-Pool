# CC: Name of compiler
# CFLAGS: flags to pass to compiler
# LIBS: libraries in use
CC = clang
CFLAGS = -Wall -pedantic -std=c99
LIBS = -lm

all: A2Test

# Testing file
A2Test: _phylib.so

# position independent target for use in shared library
phylib.o: phylib.c phylib.h
	$(CC) $(CFLAGS) -fPIC -c phylib.c -o phylib.o

# shared library
libphylib.so: phylib.o
	$(CC) -shared phylib.o -o libphylib.so $(LIBS)

phylib_wrap.c: phylib.i
	swig -python phylib.i

phylib.py: phylib.i
	swig -python phylib.i

phylib_wrap.o: phylib_wrap.c phylib.py
	$(CC) $(CFLAGS) -c phylib_wrap.c -I/usr/include/python3.11 -fPIC -o phylib_wrap.o

_phylib.so: libphylib.so phylib_wrap.o
	$(CC) $(CFLAGS) -shared phylib_wrap.o -L.  -L/usr/lib/python3.11 -lpython3.11 -lphylib -o _phylib.so

# convenience target to remove results of build
clean:
	rm -f *.o *.so phylib_wrap.c phylib.py
