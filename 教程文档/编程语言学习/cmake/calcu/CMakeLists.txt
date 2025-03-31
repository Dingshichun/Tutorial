cmake_minimum_required(VERSION 3.8)
project(calculator)
include_directories(../include) # 指定到哪里找头文件
set(LIBRARY_OUTPUT_PATH ../lib) # 设置库的输出路径，如果使用 WSL ，需要使用挂载的路径，
file(GLOB src_list ./*.cpp) # 搜索所有 cpp 文件用于生成库
add_library(calcu_shared SHARED ${src_list}) # 生成动态库