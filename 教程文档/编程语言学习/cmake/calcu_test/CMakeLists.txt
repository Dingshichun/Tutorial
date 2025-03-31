cmake_minimum_required(VERSION 3.8)
project(calcu_test)
set(EXECUTABLE_OUTPUT_PATH ../bin) # 设置可执行文件的输出路径，如果使用 WSL ，需要使用挂载的路径，
include_directories(../include) # 指定在哪找头文件
file(GLOB src_list ./*.cpp) # 搜索所有 cpp 文件用于生成可执行文件
add_executable(main ${src_list}) # 生成可执行文件 main
link_directories(../lib) # 指定到哪寻找库
target_link_libraries(main calcu_shared) # 将动态库 calcu_shared 链接到可执行文件 main