CC = g++
FLAGS = -std=c++14 -shared -fPIC -O2
INC = $(shell pkg-config --cflags python3)
INC += -I../third_party/pybind11/include
LIB = $(shell pkg-config --libs python3)

all: example1.so example2.so example3.so example4.so

example1.so: bind_class.cc
	$(CC) $< -o $@ $(FLAGS) $(INC) $(LIB)

example2.so: bind_raw_matrix.cc
	$(CC) $< -o $@ $(FLAGS) $(INC) $(LIB)

example3.so: numpy2matrix.cc
	$(CC) $< -o $@ $(FLAGS) $(INC) $(LIB)

example4.so: pyarray.cc
	$(CC) $< -o $@ $(FLAGS) $(INC) $(LIB)
