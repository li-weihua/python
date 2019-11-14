cmake_minimum_required(VERSION 3.9)

project(python_call_cpp CXX)

set(PYBIND11_CPP_STANDARD -std=c++11)

add_subdirectory(pybind11)

pybind11_add_module(example_add add.cc)
