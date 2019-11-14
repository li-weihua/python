#include <string>

#include <pybind11/pybind11.h>
namespace py = pybind11;

// This example demonstates how to bind function template
// and overloaded functions
template <typename T>
T add(T x, T y) {
  return x + y;
}

std::string add(std::string s1, std::string s2) {
  return s1 + s2;
}

int add(int x, int y, int z) {
  return x + y + z;
}

PYBIND11_MODULE(example_add, m) {
    m.def("add", &add<int>, "Add two int numbers");
    m.def("add", &add<float>, "Add two float numbers");
    m.def("add", (std::string (*)(std::string, std::string))&add, 
            "Add two strings");
    m.def("add", (int (*) (int, int, int))&add, "Add tree int numbers");
}

