# gcc/g++ 教程
## (1) 基础
编译的完整过程是从预处理、编译、汇编到链接，预处理负责宏替换，编译生成汇编，汇编生成可执行的机器码，链接将库链接到可执行文件，
### (1.1) 编译过程
编译流程：预处理——编译——汇编——链接。c 和 c++ 一样，只是命令分别是 gcc 和 g++
```
# 1、预处理。将头文件展开，宏替换，去掉注释
# -E 是预处理选项，让编译器在预处理结束后停止编译过程，-o 是指定预处理之后生成的文件名
g++ -E main.cpp -o main.i

# 2、编译。将 c 或 c++ 文件变为汇编文件
# -S 将 c 或 c++ 变为汇编文件，-o 是指定编译之后生成的汇编文件名
g++ -S main.i -o main.s

# 3、汇编。把汇编文件变为二进制文件
# -c 指的是生成目标文件，这里是将汇编变成二进制，-o 是指定汇编后生成的二进制文件名
g++ -c main.s -o main.o

# 4、链接。把函数库中的相应代码组合到目标文件中
# -o 指定生成的目标文件名
g++ main.o -o main

# 5、也可以直接一步生成可执行文件
#  直接将源文件 main.cpp 编译为可执行文件 main ，main 可直接执行。
g++ main.cpp -o main
# 执行时要加路径，比如 ./main
```
### (1.2) 静态库和动态库
* 静态库是指编译链接时，把库文件的代码全部加入到可执行文件中,因此生成的文件比较大，但在运行时也就不再需要库文件了，其后缀名一般为".a"。但是多个文件引用库文件会占用较大的空间

* 动态库在编译链接时并没有把库文件的代码加入到可执行文件中，而是在程序执行时链接文件加载库，这样可以节省系统的开销。动态库一般后缀名为".so"。

* gcc 在编译时默认使用动态库。完成了链接之后，gcc 就可以生成可执行文件，如下所示：gcc hello.o –o hello。

* gcc 默认生成的二进制程序，是动态链接的，这点可以通过 file 命令验证。
### (1.3) gcc/g++ 选项
选项记忆技巧：编译带选项时，可以联想到键盘上的 ESC 键，就是左上角的退出键，-E，-S，-c，然后依次生成的文件可以联想到下载 linux 系统提供的 .iso 镜像文件，依次为 .i-----.s-----.o 。
```
-E 只激活预处理，这个不生成文件，你需要把它重定向到一个输出文件里面。
-S 编译到汇编语言不进行汇编和链接。
-c 编译到目标代码。只激活预处理,编译,和汇编,也就是他只把程序做成 obj 文件
-o 指定输出到哪个文件。
-g 生成调试信息。GNU 调试器可利用该信息。
-static 此选项对生成的文件采用静态链接，生成的文件相比动态链接的要更大。
-shared 创建动态库，生成文件比较小，但是需要系统调用动态库。
-O0、-O1、O2、-O3 编译器的优化选项的4个级别，-O0表示没有优化,-O1为缺省值，-O3优化级别最高。
-w 不生成任何警告信息。
-W 只生成编译器认为会报错的信息。
-Wall 生成所有警告信息。
-I 路径: 提供编译时所需头文件路径。
-L 路径：添加链接库目录，使链接器能够找到库文件。
-l 库文件：链接库文件，指定要链接的库文件，例如：-l mylib。
```
**选项使用示例，重点是 -static 和 -shared**：
-static 和 -shared
```
如果想创建一个动态链接库，可以使用 GCC 的 -shared 选项。输入文件可以是源文件、汇编文件或者目标文件。
另外还得结合 -fPIC 选项。-fPIC 选项作用于编译阶段，告诉编译器产生与位置无关代码（Position-Independent Code）；这样一来，产生的代码中就没有绝对地址了，全部使用相对地址，所以代码可以被加载器加载到内存的任意位置，都可以正确的执行。这正是共享库所要求的，共享库被加载时，在内存的位置不是固定的。

例如，从源文件 add.cpp 生成动态链接库 libadd.so
g++ -fPIC -shared add.cpp -o libadd.so

还可以从目标文件 add.o 生成动态链接库 libadd.so
g++ -fPIC -c add.cpp -o add.o # 先生成目标文件，-fPIC 在生成目标文件阶段使用
g++ -shared add.o -o libadd.so # 用目标文件生成动态库

如果希望将一个动态链接库链接到可执行文件，那么需要在命令行中列出动态链接库的名称，具体方式和普通的源文件、目标文件一样。请看下面的例子：
g++ main.cpp libadd.so -o main

将 main.cpp 和 libadd.so 一起编译成 main，当 main 运行时，会动态地加载链接库 libadd.so。前提是要确保程序在运行时可以找到这个动态链接库。你可以将链接库放到标准目录下，例如 /usr/lib，或者设置一个合适的环境变量，例如 LIBRARY_PATH。不然直接执行会显示找不到动态库。  
注意，使用 -static 和 -shared 选项生成的库，其链接到可执行程序的方式和 ar 命令的方式不一样，需要将要链接的库放到标准目录或设置环境变量，不然即使生成了可执行程序，在执行可执行程序时仍会显示找不到链接库。
```
其它示例
```
# 1、编译单个源文件并生成可执程序
g++ main.cpp -o main

# 2、编译多个源文件并生成可执程序
g++ main1.cpp main2.cpp -o main

# 3、指定 c++ 标准版本
g++ -std=c++11 main.cpp -o main

# 4、-I 指定编译时所需头文件路径，-l 链接库文件，-L 添加链接库目录，使链接器可以找到库文件
g++ -I include_dir -l static_lib -L ./lib main.cpp -o  main

# 5、生成调试信息
g++ -g main.cpp -o main
```
### (1.4) g++ 链接静态库和动态库
示例文件结构如下。main.cpp 是主程序， main.o 和 main 是 main.cpp 生成的目标文件和可执行文件  
add 文件夹中有头文件 add.h 和函数 add.cpp ，还有 add.cpp 生成的二进制目标文件 main.o ，  
其它两个是 add.cpp 生成的静态库 libstatic_add.a 和动态库 libshared_add.so ，  
注意文件名前面的 lib 只是表示这是一个库文件，真实文件名是后面的 static_add.a 和 shared_add.so ，  
如果不加上 lib 的话后面链接库文件时会提示找不到文件。

这里将 add.cpp 生成的静态库和动态库链接到 最后生成的可执行程序 main 。
```
learn_g++
  |——main.cpp
  |——main.o
  |——main
  |——add
      |——add.h
      |——add.cpp
      |——add.o
      |——libstatic_add.a
      |——libshared_add.so
```
主要代码内容如下
```c++
// main.cpp
#include<iostream>
#include"./add/add.h" 
using namespace std;

int main()
{
    int a = 80;
    int b = 8;
    cout<<"a + b = "<<add(a,b)<<endl;
    return 0;
}

// add.h
int add(int,int);

// add.cpp
#include"add.h"
int add(int a,int b)
{
    return a + b;
}
```

**生成和链接静态库**
进入 learn_g++/add/ 文件夹，打开终端执行以下命令生成静态库 libstatic_add.a
```
# 首先将 add.cpp 文件编译成二进制目标文件 add.o
g++ -c add.cpp -o add.o

# 然后使用 ar(archive,归档) 命令将编译生成的 add.o 文件打包成静态库文件 libstatic_add.a
ar rcs libstatic_add.a add.o
```

然后进入 learn_g++ 目录，执行以下命令生成可执行程序 main ，并将静态库 libstatic_add.a 链接到 main
```
# -o 指定可执行程序文件名， -L 指定要链接的库所在目录，-l 指定要链接的库文件
# 注意，这里链接库文件时只需要写 static_add ，不用写前缀 lib 和后缀 .a ，不然会提示找不到文件
g++ main.cpp -o  main -L ./add -l static_add

# 生成的 main 就是链接了静态库 libstatic_add.a 的可执行文件
```

**生成和链接动态库**
进入 learn_g++/add/ 文件夹，打开终端执行以下命令生成动态库 libshared_add.so
```
# 首先将 add.cpp 文件编译成二进制目标文件 add.o
g++ -c add.cpp -o add.o

# 然后使用 ar 命令将编译生成的 add.o 文件打包成动态库文件 libshared_add.so
ar rcs libshared_add.so add.o
```

然后进入 learn_g++ 目录，执行以下命令生成可执行程序 main ，并将动态库文件 libshared_add.so 链接到 main
```
# -o 指定可执行程序文件名， -L 指定要链接的库所在目录，-l 指定要链接的库文件
# 注意，这里链接库文件时只需要写 shared_add ，不用写前缀 lib 和后缀 .so ，不然会提示找不到文件
g++ main.cpp -o  main -L ./add -l shared_add

# 生成的 main 就是链接了动态库 libshared_add.so 的可执行文件
```