# CMake 的使用
cmake 是方便编译、链接代码的工具。Linux 中编译 c 和 c++ 分别使用 gcc 和 g++ 编译器。  
虽然可以使用 gcc 或 g++ 单独编译 c 或 cpp 文件，生成可执行文件，但只是针对文件较简单的情况，文件分布比较复杂的情况下很不方便，而 cmake 就可解决该问题，cmake 编写脚本来执行**预处理、编译、汇编、链接**等过程，可以说是将这些过程隐藏了。  
cmake 主要是执行 CMakeLists.txt 脚本，从一个文件中的 CMakeLists.txt 可以找到其它文件中的 CMakeLists.txt ，只要将文件以子目录的方式添加到要执行的 CMakeLists.txt 即可，最后执行完所有 CMakeLists.txt 即可。  
编写完所有的 CMakeLists.txt 后，需要执行 cmake 和 make ，才能编译并生成可执行程序。  
执行 cmake 需要指定第一个 CMakeLists.txt 的路径，执行后生成的文件中有 makefile 文件夹，  
make 命令就是根据 makefile 文件夹中的内容来生成可执行程序。
## (1) cmake 初级
### (1.1) cmake 基础使用
安装 cmake、gcc、g++ ，打开终端执行以下代码。
```
sudo apt install cmake gcc g++
```

假如有如下已经编写好的代码：  
包括头文件 add.h 、函数文件 add.cpp 、主文件 main.cpp 以及 CMakeLists.txt
```c++
// 此处代码所在文件夹为 project/lesson_1/

// 头文件 add.h 
int add(int ,int );

// add.cpp
int add(int a,int b)
{
    return a + b;
}

// main.cpp
# include "add.h"
# include<iostream>
using namespace std;

int main()
{
    int a = 3;
    int b = 4;
    cout<<"a + b = "<<add(a,b)<<endl;
    return 0;
}
```

```cmake
# CMakeLists.txt ，所在文件夹为 project/lesson_1/ 。

# add_executable 函数增加需要编译的程序文件名， main.cpp 和 add.cpp 是 lesson_1 文件夹中的代码，  
# 不需要加入头文件，因为头文件在预处理阶段会自动被复制到对应的 cpp 文件中。
# lesson1_1 是最后生成的可执行文件名
add_executable(lesson1_1 main.cpp add.cpp)
```

然后，在 project 文件夹下也创建 CMakeLists.txt 
```cmake
# project 文件夹中的 CMakeLists.txt 

# 版本要求
cmake_minimum_required(VERSION 3.8)

# 项目名
project(learn_cmake)

# 增加要编译的子目录 lesson_1 ，由于当前的 CMakeLists.txt 在 project 文件夹中
# lesson_1 文件夹也在 project 文件夹中， CMakeLists.txt 编译时首先在当前目录，
# 即 project 中编译，所以子目录只需要写 lesson_1 ,当然也可以写绝对路径。
# 编译时会找到子目录 lesson_1 中的 CMakeLists.txt 进行编译
add_subdirectory(lesson_1)

# 子目录当然可以添加任意多个

# 执行编译，由于该语句写在 lesson_1 文件夹的 CMakeLists.txt 中，这里就不用再写。
# 如果要在这里写则需要注意路径，是 lesson_1 文件夹中的代码
# add_executable(lesson1_1 ./lesson_1/main.cpp ./lesson_1/add.cpp)
```

最后依次执行 cmake 和 make
```
# 在 project 文件夹中创建 build 文件夹（用来存放编译得到的内容），进入 build 文件夹
# 在 build 文件夹中打开终端，先执行 "cmake .."（表示执行上一级目录中的 CMakeLists.txt） ，再执行 make 。
# 具体操作如下：

# 打开 project 文件夹，在此进入终端，依次输入命令

# 创建 build 文件夹
mkdir build

# 进入 build 文件夹
cd build 

# 执行上一级目录，即 project 中的 CMakeLists.txt
cmake ..

# 生成可执行文件 
make 
```
最后会生成项目名为 lesson1_1 的可执行文件，其路径为 project/build/lesson_1/lesson1_1

### (1.2) **cmake 的静态库和动态库**
1. 引入静态库和动态库的区别
* 引入静态库时，静态库在链接阶段会被链接到最终目标中(比如可执行执行程序中)，  
缺点就是同一份静态库如果被不同的程序引用，那么内存中会存在这个静态库函数的多份拷贝。  
将静态库链接到可执行程序之后，删除静态库也不会影响可执行程序的运行。
* 引入动态库时，链接阶段不会被拷贝最终目标中，程序运行时将按照指定的规则(上一步提到的规则，并非编译时的动态库路径)  
去搜索这个动态库，搜索到了之后才加载到内存中。所以多个程序就算引用了同一个动态库，内存中也只是存在一份动态库函数的拷贝

2. 静态库的生成和链接到可执行程序
有文件结构如下，过程是将 add.cpp 函数生成静态库，然后链接到生成的可执行程序中。
```
static_lib
    |—— build
    |—— CMakeLists.txt
    |—— lesson2_3
            |—— CMakeLists.txt
            |—— main.cpp
            |—— lib
            |    |—— add.h
            |
            |—— add
                  |—— add.h
                  |—— add.cpp
                  |—— CMakeLists.txt
                  |—— build
```

各文件的代码如下：
```
# add 文件夹中的 add.h、add.cpp 和 CMakeLists.txt
# add.cpp
int add(int a,int b)
{
    return a+b;
}

# add.h
int add(int,int);

# add/CMakeLists.txt
# LIBRARY_OUTPUT_PATH 用于设置所生成的库的保存路径，PROJECT_BINARY_DIR 是环境变量，是构建树顶级目录的完整路径
# 这里是 /static_lib/build/lesson2_3/lib ，其中 build 是用于存放编译内容的目录，lesson2_3 是用于生成可执行程序的 CMakeLists.txt 的上一级目录
set(LIBRARY_OUTPUT_PATH ${PROJECT_BINARY_DIR}/lib) 

# 使用 add.cpp 函数生成一个静态链接库 static_lib 和动态链接库 shared_lib
# 生成的库名前面会默认有 lib ，表示是库文件，即 libstatic_lib.a 和 libshared_lib.so
add_library(static_lib STATIC add.cpp) # 生成静态库，标志是 STATIC
add_library(shared_lib SHARED add.cpp) # 生成动态库，标志是 SHARED

# lesson2_3 文件夹下的 main.cpp、CMakeLists.txt 和 lib 中的 add.h
# lesson2_3/main.cpp
# 下面两行的 "#" 是包含文件，不代表注释
# include<iostream>
# include "add.h" // 这里的 add.h 是在 lib 文件夹中，所以在 CMakeLists.txt 中要指定包含头文件的相对路径"./lib"
using namespace std;

int main()
{
    int a = 3;
    int b = 4;
    cout<<"result is : "<<add(a,b)<<endl;
    return 0;
}

# lesson2_3/CMakeLists.txt
add_subdirectory(./add) # 增加子文件夹 add ，编译时寻找其中的 CMakeLists.txt 编译
include_directories(./lib) # 指定头文件包含路径
add_executable(lesson2_3 main.cpp) # 生成可执行文件 lesson2_3

# 注意只写库名就可以，不用写全部的绝对路径，且链接静态库的步骤要在 add_executable() 生成可执行程序之后。
# lesson2_3 是要链接到的可执行程序名
link_directories(填写保存库的路径) # 注意，自定义的库要链接库所在目录，不然系统找不到库
target_link_libraries(lesson2_3 "这里填写生成的静态库 libstatic_lib.a 的库名，即  static_add") 

# lesson2_3/lib/add.h
int add(int,int);

# static_lib 文件夹中的 CMakeLists.txt
# static_lib/CMakeLists.txt
add_subdirectory(./lesson2_3) # 添加子文件夹 lesson2_3
```

将库链接到可执行程序 lesson2_3 
根据上面设定的库保存路径可知 
生成的静态库路径是 `/static_lib/build/lesson2_3/lib/libstatic_lib.a`
生成的动态库路径是 `/static_lib/build/lesson2_3/lib/libshared_lib.so`
库文件名前面的 lib 只是表明这是一个库，实际名字不用加 lib
**将两个库名（注意只需要库名，不用全部路径，不然会出错，不知道为什么）**填入 lesson2_3/CMakeLists.txt 中，再次执行编译即可生成可执行程序 lesson2_3 ，即
```
target_link_libraries(lesson2_3 static_lib)
target_link_libraries(lesson2_3 shared_lib)
```

链接库也可以使用 link_libraries()，但只能链接静态库，且要写在 add_executable() 之前。不推荐使用该方法。
```
link_directories(/home/dsc/lib) # 链接到库所在的目录。注意，如果是自定义的库，不指定目录的话系统找不到。
link_libraries(static_lib) # 链接库，只需要写库名即可
```
最后生成的可执行程序 lesson2_3 路径为 /static_lib/build/lesson2_3/lesson2_3

### (1.3) cmake 安装库
### (1.4) cmake 搜索文件
使用 add_executable() 时，如果添加的源程序较多，逐个添加很麻烦且不方便，就可以使用搜索文件。  
```cmake
# 方法 1 
# 使用 aux_source_directory(目录名 变量名) 查找某个目录中的所有源文件，并将结果保存到变量中。
aux_source_directory(./main/dsc src_list) # 查找所有源文件，并保存到变量 src_list
add_executable(main ${src_list}) # 再把变量 src_list 的值传递给 add_executable()

# 方法 2 ，使用搜索文件命令 file
# 格式: file(GLOB或GLOB_RECURSE 变量名 搜索路径和文件类型)
# GLOB 选项：将搜索到的满足条件的文件名生成一个列表，并存储到变量中
# GLOB_RECURSE:递归搜索指目录，将搜索到的满足条件的文件名生成一个列表，并存储到变量中
file(GLOB src_list ./main/dsc/*.cpp) # 搜索所有 cpp 文件，生成列表，并保存到变量 src_list
file(GLOB_RECURSE hpp_list ./main/dsc/*.h) # 递归搜索 dsc/ 目录，生成列表，并保存到变量 hpp_list

```

## (2) cmake 语法
### (2.1) cmake 打印和变量设置
cmake 的文件是以 cmake 或 txt 为后缀，比如 first.cmake 、CMakeLists.txt ，在编译时是从第一个 CMakeList.txt 或 CMakeLists.cmake 开始执行，寻找其它 CMakeList.txt 或 CMakeLists.cmake 进行编译。  
单独执行 cmake 文件的方式是 `cmake -P cmake文件` ，比如：cmake -P first.cmake 。  
1. **cmake 打印命令 message** 
```cmake
message("hello") # 打印单行
# 打印多行，将内容放在两个方括号中，并分行。
message([[hello world,
welcome to China!
game over !
]])
```
message 命令的常用选项
```
无选项          表示是重要消息
STATUS          非重要消息
WARNING         cmake 警告，会继续执行
AUTHOR_WARNING  cmake 警告(dev)，会继续执行
SEND_ERROR      cmake 错误，会继续执行，会跳过生成的步骤
FATAL_ERROR     cmake 错误，终止所有处理过程
```
message 常用选项使用示例
```cmake
message("it is import") # 不带任何选项，表示是重要消息
message(STATUS "it's not import") # STATUS 表示非重要消息
message(FATAL_ERROR "cmake error,it will stop all procession") # 会终止所有处理过程
```
2. **cmake 变量设置 set**  
cmake 变量包括系统变量和自定义变量，区分大小写，在存储时默认都是字符串。  
对变量的基本操作是 set 和 unset ，也可以使用 list 或 string 操作变量。  
取变量值：${变量名}   
set 的用法如下,set 设置的变量默认是字符串类型
```cmake
set(num 99) # 将变量 num 的值设为 99
set([[name]] "dsc") # 将变量名放在两个方括号中
message("${num},${name}") # 输出:99,dsc

# 设置环境变量
set(ENV{CXX} "g++") # CXX 代表 g++ , ENV 指环境变量，在当前项目有效。
message($ENV{CXX}) # 输出:g++
unset(ENV{CXX}) # 删除环境变量 CXX ，再打印会报错。

# 设置文件输出路径
# 设置可执行文件的输出路径,EXECUTABLE_OUTPUT_PATH 是系统变量
set(EXECUTABLE_OUTPUT_PATH /home/exe) 
set(CMAKE_CXX_STANDARD 11) # 设置 c++标准， CMAKE_CXX_STANDARD 是系统变量
set(LIBRARY_OUTPUT_PATH /home/lib) # 设置库文件的输出路径
```
3. **cmake 变量设置 list**  
cmake 中 set 和 list 均可设置变量
```cmake
# 给一个变量赋多个值，相当于这个变量是一个列表
set(LISTVALUE val1 val2 val3) # 用空格隔开，也可以用分号隔开，相当于 LISTVALUE=[val1,val2,val3]
message(${LISTVALUE}) # 输出:val1val2val3 。注意输出会紧邻，没有空格。

# list 方法给一个变量赋多个值时要使用 APPEND ，不能直接赋值。
list(APPEND ARRAY 12 34 54 66) # 相当于 ARRAY=[12,34,54,66]
message(${ARRAY}) # 输出:12345466 。输出没有间隔

# 获取数组的长度，用 LENGTH
list(LENGTH ARRAY len) # LENGTH 表示获取长度，获取变量 ARRAY 的长度保存到变量 len
message(${len}) # 输出:4 。ARRAY 中保存有 4 个数

# 查找数组中的值，用 FIND
list(APPEND NUM 44 55 66)
list(FIND NUM 33 index) # 使用 FIND 在 NUM 中查找 33 ，结果保存到 index 中 ，查找成功则返回对应的索引，数组索引从 0 开始，失败返回 -1 。
message(${index}) # 输出：-1

# 删除数组中的值，用 REMOVE_ITEM
list(APPEND NAME dsc ss dd)
list(REMOVE_ITEM NAME dsc)
message(${NAME}) # 输出:ssdd 。输出没有间隔

# 添加和插入，末尾添加可用 APPEND,根据位置插入用 INSERT
list(APPEND ARR 32 44)
list(APPEND ARR1 99 88 77)
list(APPEND ARR 55) # 添加 55 到数组末尾
message(${ARR}) # 输出:324455
list(INSERT ARR1 1 66) # 在 ARR1 的位置 1 ，也就是 99 后面添加 66
message(${ARR1}) # 输出:99668877

# 反转(REVERSE)和排序(SORT)
list(APPEND NUM1 99 44 77 66)
list(REVERSE NUM1) # 反转
message(${NUM1}) # 输出:66774499
list(SORT NUM1) # 排序
message(${NUM1}) # 输出:44667799
```
### (2.2) cmake if 语句
```cmake
# 1、if 语句，和其它语言类似，注意条件的括号和 endif()
#[[
if(条件 1)
   语句 1
elseif(条件 2)
   语句 2
else()
   语句 3
endif()
]]

# 示例：
set(VAL TRUE)
if(VAL)
    message("it is true")
else()
    message("it is false")
endif()

# cmake 比较运算符： LESS、GREATER、EQUAL、GREATER_EQUAL、LESS_EQUAL
# cmake 逻辑运算符： AND、OR、NOT
if(3 GREATER_EQUAL 3)
    message("3 >= 3")
endif()
if(NOT 3 AND 3)
    message("3 AND 3 is FALSE")
else()
    message("3 AND 3 is TRUE")
endif()
```

### (2.3) cmake 循环控制
主要是 for 和 while ，推荐 for
```cmake
# for 用法 1: 
#[[
foreach(循环值 RANGE 最大值)
endforeach()
]]

# RANGE 默认从 0 开始，步长为 1 ，包括最大值 3 。输出:0 1 2 3
foreach(VAR RANGE 3) 
    message(${VAR})
endforeach()

# for 用法 2:
#[[
foreach(循环值 RANGE 最小值 最大值 步长)
endforeach()
]]
# 最小值 1 ，最大值 5 ，包括 5 ，步长 2 。输出: 1 3 5
foreach(VAL RANGE 1 5 2) 
    message(${VAL})
endforeach()

# for 用法 3:
#[[
foreach(循环值 IN LISTS 列表名 ITEMS 要加入循环的items)
endforeach()
]]

list(APPEND MY_LIST 22 33 44 99) # 生成列表 MY_LIST
# 循环值 VAL 在列表 MY_LIST 中，再加上额外的 108 和 end 。输出:22 33 44 99 108 end
foreach(VAL IN LISTS MY_LIST ITEMS 108 end)
    message(${VAL})
endforeach()
```
### (2.4) cmake 函数
cmake 函数定义格式
```cmake
function(function_name arg1 arg2 …… argn)
    commands
endfunction()
```
cmake 函数的相关变量
```cmake
# ARGC 是参数数量， ARGV 是保存所有参数的列表， ARGV0、ARGV1、ARGV2 …… ARGVn 代表第 0~ n 个参数
```
### (2.5) cmake 宏
cmake 宏的定义方式
```cmake
# 方式 1 :使用 gcc/g++ 编译时指定
g++ main.cpp -DDEBUG -o main # 其中 -D 选项是定义宏，宏名字为 DEBUG 

# 方式 2 :在 CMakeLists.txt 中定义
add_definitions(-DDEBUG) # 定义一个名为 DEBUG 的宏
```
## (3) 嵌套的 cmake
### (3.1) 简介
如果项目比较复杂，有较多源文件和库，那么把所有内容都写到一个 CMakeLists.txt 文件中会较为复杂，  
不方便后续的维护和修改，所以就有嵌套的 cmake。  
嵌套的 cmake 就是在项目根目录的 CMakeLists.txt 中添加其它源文件或库所在的目录，那么在执行编译时，  
就会从根目录的 CMakeLists.txt 开始执行，找到所添加目录中的 CMakeLists.txt ，逐层进行编译。  
当然，除了根目录，其它目录中的 CMakeLists.txt 也可以包含目录。  
简单说，就是复杂的问题简单化，将项目分割变小，方便维护修改。

在根目录的 CMakeLists.txt 中定义的变量相当于全局变量，其所包含目录中的 CMakeLists.txt 也可使用，  
其它目录中的 CMakeLists.txt 所定义的变量相当于局部变量，作用域只是当前目录。  

添加子目录的命令是:add_subdirectory(path) ,子目录中要有 CMakeLists.txt 文件。
### (3.2) 嵌套 cmake 实例
文件结构如下。简单的加、减、乘函数，将其生成为库，然后链接测试。  
build 文件夹存放编译内容， bin 文件夹存放生成的可执行文件， lib 文件夹存放生成的库  
include 文件夹存放头文件， calcu_test 文件夹是测试加、减、乘函数的文件夹，使用其中 main.cpp 生成可执行程序  
calcu 文件夹存放函数，用来生成库。
```
cmake_project
    |—— build
    |—— bin
    |—— lib
    |—— CMakeLists.txt
    |—— include
    |       |—— calcu.h
    |
    |—— calcu_test
    |       |—— CMakeLists.txt
    |       |—— main.cpp
    |
    |—— calcu
         |—— add.cpp
         |—— minu.cpp
         |—— multi.cpp
         |—— CMakeLists.txt     
```
按照文件夹从上到下的顺序，需要编写的文件内容如下：
```cmake
# 1、cmake_project/CMakeLists.txt
cmake_minimum_required(VERSION 3.8) 
project(calcu1)
add_subdirectory(./calcu) # 包含两个子目录
add_subdirectory(./calcu_test)

# 2、cmake_project/include/calcu.h
# 三个函数的声明
int add(int,int);
int minu(int,int);
int multi(int,int);

# 3、cmake_project/calcu_test/CMakeLists.txt
cmake_minimum_required(VERSION 3.8) 
project(calcu_test)
include_directories(../include) # 指定头文件包含路径，即到哪里找头文件
file(GLOB src_list ./*.cpp) # 查找 .cpp 文件名字并保存到变量 src_list ，用于生成可执行程序
set(EXECUTABLE_OUTPUT_PATH ~/Downloads/cmakePractise/bin) #  设置库文件的输出路径
add_executable(calcu_test ${src_list}) # 添加可执行程序
link_directories(../lib) # 库的链接目录
target_link_libraries(calcu_test calcu_static) # 将库链接到可执行程序
```
```c++
// 4、cmake_project/calcu_test/main.cpp
#include<iostream>
#include"calcu.h"
using namespace std;

int main()
{
    int a = 9;
    int b = 8;
    cout<<"a + b = "<<add(a,b)<<endl;
    cout<<"a - b = "<<minu(a,b)<<endl;
    cout<<"a * b = "<<multi(a,b)<<endl;
    return 0;
}

// 5、cmake_project/calcu 中的 add、minu、multi 函数
// add.cpp
#include"calcu.h"
int add(int a,int b){return a + b;}

// minu.cpp
#include"calcu.h"
int minu(int a,int b){return a - b;}

// multi.cpp
#include"calcu.h"
int multi(int a,int b){return a * b;}
```
```cmake
# 6、cmake_project/calcu/CMakeLists.txt
cmake_minimum_required(VERSION 3.8)
project(calculator)

file(GLOB calcu_list ./*.cpp) # 查找所有 .cpp 文件名字保存到 calcu_list 用于生成库
include_directories(../include) # 指定头文件包含路径
set(LIBRARY_OUTPUT_PATH ~/Downloads/cmakePractise/lib) # 设置库文件的输出路径
add_library(calcu_static STATIC ${calcu_list}) # 生成静态库 calcu_static
```
完成以上代码后进入 build 文件夹，依次执行命令 cmake 和 make
```
cmake .. # 编译
make # 生成可执行文件
```
因为指定了文件夹，所以最后生成的静态库 libcalcu_static 在 lib 文件夹中，可执行文件 calcu_test 在 bin 文件夹中，  
**库也可以链接到库，如静态库链接到静态库，动态库链接到静态库，方法和上面类似。**