cmake_minimum_required(VERSION 3.21)
project(chunkscore_cpp LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(_textscore_cpp src/textscore_cpp.cpp)

install(TARGETS _textscore_cpp DESTINATION chunkscore)
