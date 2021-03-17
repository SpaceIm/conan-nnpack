cmake_minimum_required(VERSION 3.4)
project(cmake_wrapper)

include(conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

add_library(cpuinfo INTERFACE IMPORTED)
set_property(TARGET cpuinfo PROPERTY INTERFACE_LINK_LIBRARIES CONAN_PKG::cpuinfo)

add_library(pthreadpool INTERFACE IMPORTED)
set_property(TARGET pthreadpool PROPERTY INTERFACE_LINK_LIBRARIES CONAN_PKG::pthreadpool)

add_library(fxdiv INTERFACE IMPORTED)
set_property(TARGET fxdiv PROPERTY INTERFACE_LINK_LIBRARIES CONAN_PKG::fxdiv)

add_library(psimd INTERFACE IMPORTED)
set_property(TARGET psimd PROPERTY INTERFACE_LINK_LIBRARIES CONAN_PKG::psimd)

add_library(fp16 INTERFACE IMPORTED)
set_property(TARGET fp16 PROPERTY INTERFACE_LINK_LIBRARIES CONAN_PKG::fp16)

add_subdirectory(source_subfolder)

if(CMAKE_SYSTEM_NAME STREQUAL "Linux")
    target_link_libraries(nnpack PRIVATE m)
endif()
