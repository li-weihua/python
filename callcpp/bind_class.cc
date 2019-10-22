#include <pybind11/pybind11.h>
namespace py = pybind11;

struct Pet {
    Pet(const std::string &name) : name(name) { }
    void setName(const std::string &name_) { name = name_; }
    const std::string &getName() const { return name; }

    std::string name;
};

struct Point {
  Point(int x_, int y_): x(x_), y(y_) {}
  int x, y;
};

int sum(Point p) {
  return p.x + p.y;
}

PYBIND11_MODULE(example1, m) {
    py::class_<Pet>(m, "Pet")
        .def(py::init<const std::string &>())
        .def("setName", &Pet::setName)
        .def("getName", &Pet::getName);

    py::class_<Point>(m, "Point")
        .def(py::init<int, int>());
    
    m.def("sum", &sum, "A function which adds two numbers");
}

