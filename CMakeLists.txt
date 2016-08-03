#
# Very simple setup.
#
cmake_minimum_required(VERSION 2.8.3)
project("Documentation Test with Namespace arbitrary")
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
add_executable(doc-test-exe
               include/arbitrary/common.h
               include/arbitrary/BaseClass.h
               include/arbitrary/DerivedClass.h
               include/OuterFile.h
               src/main.cpp
)
