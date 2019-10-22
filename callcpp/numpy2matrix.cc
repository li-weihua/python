#include <pybind11/pybind11.h>
namespace  py = pybind11;

class Matrix {
public:
    Matrix(float *ptr, ssize_t rows, ssize_t cols) : 
      m_data(ptr), m_rows(rows), m_cols(cols) {
    }

    Matrix(Matrix &&s) : m_rows(s.m_rows), m_cols(s.m_cols), m_data(s.m_data) {
    }

    ~Matrix() { }

    float operator()(ssize_t i, ssize_t j) const {
        return m_data[(size_t) (i*m_cols + j)];
    }

    float &operator()(ssize_t i, ssize_t j) {
        return m_data[(size_t) (i*m_cols + j)];
    }

    float *data() { return m_data; }

    ssize_t rows() const { return m_rows; }
    ssize_t cols() const { return m_cols; }
private:
    ssize_t m_rows;
    ssize_t m_cols;
    float *m_data;
};


PYBIND11_MODULE(example3, m) {
  py::class_<Matrix>(m, "Matrix", py::buffer_protocol())
    /// Construct from a buffer
    .def(py::init([](py::buffer const b) {
        py::buffer_info info = b.request();
        if (info.format != py::format_descriptor<float>::format() || info.ndim != 2)
            throw std::runtime_error("Incompatible buffer format!");

        auto v = new Matrix(static_cast<float*>(info.ptr), 
                            info.shape[0], info.shape[1]);
        return v;
    }))

   .def("rows", &Matrix::rows)
   .def("cols", &Matrix::cols)
   .def("__call__", [](const Matrix &m, int i, int j) {
        if (i >= m.rows() || j >= m.cols())
            throw py::index_error();
        return m(i, j);
    })
    /// Bare bones interface
   .def("__getitem__", [](const Matrix &m, std::pair<ssize_t, ssize_t> i) {
        if (i.first >= m.rows() || i.second >= m.cols())
            throw py::index_error();
        return m(i.first, i.second);
    })
   .def("__setitem__", [](Matrix &m, std::pair<ssize_t, ssize_t> i, float v) {
        if (i.first >= m.rows() || i.second >= m.cols())
            throw py::index_error();
        m(i.first, i.second) = v;
    })
   /// Provide buffer access
   .def_buffer([](Matrix &m) -> py::buffer_info {
        return py::buffer_info(
            m.data(),                               /* Pointer to buffer */
            { m.rows(), m.cols() },                 /* Buffer dimensions */
            { sizeof(float) * size_t(m.cols()),     /* Strides (in bytes) for each index */
              sizeof(float) }
        );
    })
    ;
}

