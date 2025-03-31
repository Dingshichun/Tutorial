# **linux 基础**
## （1）**常用命令**
命令的一般用法：**命令** [**选项**] [**参数**]。  
**选项** 的作用是调整命令功能。如果没有选项，那么命令只能执行最基本的功能；而一旦有选项，则可以显示更加丰富的数据。  
**参数** 是命令的操作对象，一般文件、目录、用户和进程等可以作为参数被命令操作。

* **pwd**（print working directory）。打印当前所在目录。

* **cd - 或 cd $OLDPWD** 回到上一次打开的目录

* **ls**（list）。显示文件夹中的内容，常用的是 `ls -a` ，表示显示当前目录的所有文件，包括隐藏文件。`ls -l` 以长格式显示文件和目录信息，包括权限、所有者、大小、创建时间等。

* **cd**（change directory）。打开指定文件夹。

* **mkdir**（make directory）。创建目录。

* **rmdir**（remove directory）。只能删除空目录。

* **touch** 。如果文件不存在，则会建立空文件；如果文件已经存在，则会修改文件的时间戳（访问时间、数据修改时间、状态修改时间都会改变）​。

* **rm**（remove files or directories）。是强大的删除命令，不仅可以删除文件，也可以删除目录。  
常用选项包括 -f（force，强制删除）、-r（recursive，递归删除，常用在删除目录）、-i （删除前询问），

* **mv**（move or rename）。移动或重命名文件或目录。  
一般和通配符 '*' 搭配使用，`mv *.txt ./textFiles` 将当前目录所有 txt 格式的文件移动到 textFiles 文件夹。  
`mv *.* ./textFiles` 将当前目录所有文件移动到 textFiles 文件夹。
* **tree** 。以树形结构显示目录下的文件。

* **cat**（concatenate files and print on the standard output）。合并文件并打印输出到标准输出。

* **more**（file perusal filter for crt viewin）。more 是分屏显示文件的命令，如果文件过大，则 cat 命令会有心无力，这时 more 命令的作用更加明显。

* **cp**（copy）。复制。格式是：cp 文件 目录。比如 `cp myDir.txt ./textFiles` 是将 myDir.txt 文件复制到 textFiles 文件夹。

* **find** 。查找。

* **sort** 。排序。

* **>** 。将选定内容存储到指定文件中，但是会覆盖原文件内容。比如 `ls >myDir.txt` 是将所显示的当前目录的所有文件名保存到 myDir.txt 文件中，  
`sort myDir.txt>sorted_myDir.txt` 则是将排序后的 myDir.txt 文件内容保存到 sorted_myDir.txt 文件中

* **>>** 。将选定内容追加到指定文件中，不会覆盖原文件内容。比如 `ls >>myDir.txt` 是将所显示的当前目录的所有文件名追加到 myDir.txt 文件中。

* **shutdown**。关机和重启。`shutdown -r now` 表示现在重启，reboot 也可重启。

## （2）**vim 的使用**

1. vim 三种模式：**命令、输入、编辑**。默认处于命令模式，按 i、o、a 、I、O、A 进入输入模式，最底行会显示 "INSERT" ，编辑完成后按 esc 退出输入模式。  
编辑模式可保存、查找、替换内容，在命令模式下按 ":" 进入编辑模式，输入指令执行，如 ":wq" ,执行后自动进入命令模式。  
不知道当前处于什么模式的话，多按几次 esc 即可。
2. `vim book.txt` 打开 book.txt 文件，  
（**重点**）直接在命令模式中输入 "nG" ​（n 为数字，G 为大写）或 ":n" ​（在编辑模式中输入数字）命令将光标快速地定位到指定行的行首。  
（**重点**）在 Vim 命令模式中输入 "/要查找的字符串"​，再按一下回车键，就可以从光标所在行开始向下查找指定的字符串。  
如果要向上查找，则只需输入 "​？要查找的字符串" 即可。  
命令模式下删除、粘贴和复制：
```
    x               ——删除光标所在字符
    nx              ——从光标所在位置向后删除n个字符，n为数字
    dd              ——删除整行。如果之后粘贴，则此命令的作用是剪切
    ndd             ——删除多行
    dG              ——删除从光标所在行到文件末尾的内容
    D               ——删除从光标所在处到这行行尾的内容
    :起始行，终止行d  ——删除指定范围的行
    yy或Y          ——复制单行
    nyy或nY        ——复制多行
    小写 p               ——粘贴到当前光标所在行下
    大写 P               ——粘贴到当前光标所在行上
```
3. u 表示撤销。保存和退出是在命令模式中进行，只需记住 w、q、! ，作用如下：
```
    w    ——保存不退出
    q    ——不保存退出
    !    ——强制性操作
```
命令模式输入 ":set nu" 显示文件行号，再次输入 ":set nonu" 则取消行号。

## （3）**源代码编译和执行**
1. 首先安装 **C 语言编译器 gcc 和 c++ 编译器 g++** ,执行 `sudo apt-get install gcc g++` 进行安装。  
注意编译器安装只能使用二进制包安装，不能使用源码包安装。

2. 编译运行。**C 语言编译使用 gcc ，c++ 编译使用 g++ 。**
```
    # gcc 编译并运行 hello.c 文件的过程如下：
    
    # hello.c 文件的内容是输出 hello world
    [root@localhost ~]# gcc -c hello.c
    # -c 生成 “.o” 头文件。这里会生成 hello.o 头文件，但是不会生成执行文件
    [root@localhost ~]# gcc -o hello hello.o
    # -o 生成执行文件，并指定执行文件名。这里生成的 hello 就是执行文件
    [root@localhost ~]# ./hello
    hello world
    # 执行 hello 文件，
```

## （4）**软链接和硬链接**

1. 软、硬链接的创建。
```
# 硬链接的创建，可以使用相对路径。格式： ln 源文件 目标文件
# 将 name.txt 的硬链接创建到 ./user/name-hard ， name-hard 即为硬链接。
ln ./name.txt ./user/name-hard 

# 软链接的创建，必须使用绝对路径，否则会出错。格式： ln -s 源文件 目标文件
# 将 /root/name.txt 的软链接创建到 /root/user/name-soft ， name-soft 即为软链接。
ln -s /root/name.txt /root/user/name-soft
```

2. 软、硬链接的特点
硬链接的特点如下：

* 修改源文件或是硬链接文件，另一个文件中的数据都会同步改变。

* 无论删除源文件还是硬链接文件，只要有一个还存在，该文件都可访问。

* 硬链接不会建立新的 inode 信息， 也不会更改 inode 的总数。

* **硬链接不能跨文件系统建立，也不能链接目录。**
软链接的特点如下：

* 修改源文件或是软链接文件，另一个文件中的数据都会同步改变。

* 删除软链接，源文件不受影响，但是删除源文件，软链接找不到实际数据，显示文件不存在。

* 软链接会新建自己的 inode 信息和 block ，只是在 block 中不存储实际文件数据， 而存储的是源文件的文件名及 inode 号。

* **硬链接可以跨文件系统建立，也可以链接目录。**

## （5）**权限管理命令**

1. 文件的归属情况包括 **所有者、所属组和其他**。  
权限包括 **读(r,数字表示为 4)、写(w,2)和执行(x,即 execute ,1)** ，  
权限表示为 10 个字母，比如：`-rw-r--r--` ，第一个代表文件类型，"-" 代表普通文件，  
"b" 表示块设备文件， "c" 表示字符设备文件，"d" 目录文件，"l" 软链接文件，"p" 管道符文件。  
第 2 到 10 位依次代表所有者、所属组和其他的权限。

2. 权限更改命令 chmod 。
```
# chmod 的使用
# 用户加上想要的权限
chmod u+x, g+x, o+x file

# 用户减去权限
chmod u-x, g-x, o-x file

# 直接指定权限
chmod u=rwx, g=rwx, o=rwx file

# 直接使用数字表示， r = 4 , w = 2 , x = 1 .
chmod 755 file
```

3. **读、写、执行权限对文件和目录的作用是不同的**。  

* 读权限 r  
对文件有 r 权限， 可以读取其数据，可执行 cat 、more 、less 等命令查看；  
对目录有 r 权限，可执行 ls 查看目录中的内容。  

* 写权限 w  
对文件有 w 权限，可以修改其数据，可执行 echo、vim 等修改文件数据，但是只能修改数据，不能删除文件本身，想删除需要对文件的上级目录有 w 权限；  
对目录有 w 权限，代表可以修改目录下的数据，即可以在目录中新建、删除、复制、剪切子文件或子目录，可以执行 touch、rm、cp、mv 命令。  

* 执行权限 x  
对文件有 x 权限，表示其可以运行，但能否正确执行，还需要看语言代码是否正确。  
对目录有 x 权限，表示可以进入目录，可对其执行 cd 命令。

4. 文件的所有者和所属组更改命令 chown 。
```
# chown 更改文件的所有者和所属组

# 将 file 的所有者更改为 dsc
chown dsc file

# 将 file 的所有者和所属组分别更改为 dsc 和 group
chown dsc:group file 
chown dsc.group file # ":" 也可以用 "." 代替

# chgrp 更改文件和目录的所属组

# 将 file 的所属组更改为 dsc
chgrp dsc file
```

## （6）**压缩和解压缩**

Linux 不靠拓展名区分文件，而是靠权限，压缩包命名仍带有拓展名的作用是方便解压缩，因为每种压缩方法对应的解压缩方法不一样。  
介绍 zip 和 tar ，其它命令大同小异。
```
# zip 压缩和解压缩。

压缩格式： zip 选项 压缩包名 源文件或目录
# 将文件 file.txt 和 file1.txt 压缩为 file.zip
zip file.zip file.txt file1.txt
# 将目录 file 压缩为 file.zip， 选项 r 表示递归压缩。
zip -r file.zip file

解压缩格式： unzip 选项 压缩包名
# 解压 file.zip 压缩包，得到 file 文件夹
unzip file.zip
# 选项 d 指定解压到哪个目录
unzip -d ./temp file.zip
```

linux 中打包和压缩不同，打包使用 tar 。
```
# tar 打包和解打包
# 打包格式： tar 选项 压缩包名 源文件或目录
# 选项：
#    -c:    打包
#    -f:    指定压缩包的文件名。压缩包的扩展名是用来给管理员识别格式的，所以一定
#                要正确指定扩展名
#    -v:    显示打包文件过程

# 将 file.txt 打包为 file.txt.tar
tar -cvf file.txt.tar file.txt

# 将文件 file.txt 和目录 ./temp 打包为 file.tar  
tar -cvf file.tar file.txt ./temp

# 有的压缩命令不能压缩目录，可用 tar 先打包，再压缩

# 将目录 file 打包为 file.tar 
tar -cvf file.tar file

# 将 file.tar 压缩为 file.tar.gz
gzip file.tar

解打包格式： tar 选项 压缩包
选项：
    -x:        解打包
    -f:        指定压缩包的文件名
    -v:        显示打包文件过程
    -t:        测试，就是不解打包，只是查看包中有哪些文件
    -C 目录：    指定解打包位置

# 将 file.txt.tar 解打包到当前目录
tar -xvf file.txt.tar
```

tar 命令可在打包的同时也完成压缩
```
tar 选项 压缩包 源文件或目录
选项：
    -z:    压缩和解压缩 “.tar.gz” 格式
    -j:    压缩和解压缩 “.tar.bz2” 格式

# 将目录 file 打包并压缩为 file.tar.gz
tar -zcvf file.tar.gz ./file

# 解压缩和解打包 file.tar.gz 
tar -zxvf file.tar.gz
```

## （7）**编译工具 cmake 的使用**
### （7.1）**cmake 初级**
cmake 是方便编译、链接代码的工具。
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

# 增加要编译的子目录 lesson_1 ，由于当前的 CMakeLists.txt 在project 文件夹中
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
# 在 project 文件夹中创建 build 文件夹，进入 build 文件夹
# 在 build 文件夹中打开终端，先执行 "cmake .." ，再执行 make 。
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

### （7.2）**cmake 的静态库和动态库**
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
# 使用 add.cpp 函数生成一个静态链接库 static_lib 和动态链接库 shared_lib
add_library(static_lib STATIC add.cpp) # 生成静态库
add_library(shared_lib SHARED add.cpp) # 生成动态库

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
add_subdirectory(add) # 增加子文件夹 add ，编译时寻找其中的 CMakeLists.txt 编译
include_directories(./lib) # 指定头文件包含路径
add_executable(lesson2_3 main.cpp) # 生成可执行文件 lesson2_3

# 注意是绝对路径，且链接静态库的步骤要在 add_executable() 生成可执行程序之后。
# lesson2_3 是要链接到的可执行程序名
target_link_libraries(lesson2_3 "这里填写生成的静态库 libstatic_lib.a 的绝对路径") 

# lesson2_3/lib/add.h
int add(int,int);

# static_lib 文件夹中的 CMakeLists.txt
# static_lib/CMakeLists.txt
add_subdirectory(lesson2_3) # 添加子文件夹 lesson2_3
```

首先生成静态库和动态库
进入 add 文件夹中的 build 文件夹，打开终端，依次执行以下命令。
```
cmake .. # 编译上一级目录（ add ）中的 CMakeLists.txt 
make # 注意，要执行完 make 才会生成静态库 libstatic_lib.a 和动态库 libshared_lib.so ，两个文件都在 add/build/ 中
```

然后生成可执行文件，  
生成的静态库路径是 `/static_lib/lesson2_3/add/build/libstatic_lib.a`
生成的动态库路径是 `/static_lib/lesson2_3/add/build/libshared_lib.so`
将两个路径填入 lesson2_3/CMakeLists.txt 中再次执行编译即可生成可执行程序 lesson2_3 ，即
```
target_link_libraries(lesson2_3 /static_lib/lesson2_3/add/build/libstatic_lib.a)
target_link_libraries(lesson2_3 /static_lib/lesson2_3/add/build/libshared_lib.so)
```
最后生成的可执行程序 lesson2_3 路径为 /static_lib/build/lesson2_3/lesson2_3

## (8) Linux 网络管理(网络配置和命令)
### (8.1) 网络地址配置
`ifconfig` 查看网络地址，格式 : ifconfig 或 ifconfig 网卡名
输出的第一行显示网卡状态信息，如下：  
* eth0 表示第一块网卡。

* UP 代表网卡开启状态。

* RUNNING 代表网卡的网线被接上。

* MULTICAST 表示支持组播。

第二行显示网卡的网络信息，如下：

* inet（ IP 地址）

* broadcast（广播地址）

* netmask（掩码地址）

* RX 表示接收数据包的情况，TX 表示发送数据包的情况。

* lo 表示主机的回环网卡，是一种特殊的网络接口，不与任何实际设备连接，而是完全由软件实现。与回环地址（127.0.0.0/8 或 ::1/128）不同，回环网卡对系统显示为一块硬件。任何发送到该网卡上的数据都将立刻被同一网卡接收到。

在 Linux 主机中，手工修改网络配置有两种最基本的方法：
1. 临时配置：使用命令调整网络参数
* 简单、快速，可直接修改运行中的网络参数
* 一般只适合在调试网络的过程中使用
* 系统重启以后，所做的修改将会失效

2. 固定设置：通过配置文件修改网络参数，相当于“永久配置”
* 修改各项网络参数的配置文件
* 适合对服务器设置固定参数时使用
* 需要重载网络服务或者重启以后才会生效

`ifconfig` **设置网络接口参数**
```
# 格式：ifconfig 设备名 IP netmask
ifconfig eth0 192.168.168.1/24
```

**禁用或重新激活网卡**
```
# 格式: ifconfig 网络接口 up或down
ifconfig eth0 up
ifconfig eth0 down
```

**重启 network 网络服务**：`systemctl restart network`

**网络接口配置文件**  
网络接口的配置文件默认位于目录 "/etc/sysconfig/network-scripts/" 中，文件名格式为"ifcfg-XXX" ，其中 "XXX" 是网络接口的名称，"ifcfg-ens33" ：是第一块以太网卡的配置文件，该文件中一些内容如下：  
* TYPE：设置网卡类型
* ONBOOT: 设置网络接口是否在 Linux 系统启动时自动激活
* NETMASK：设置网络接口的子网掩码
* GATEMASK：设置网络接口的默认网关地址
* DNS：设置 DNS 服务器的 IP 地址
### (8.2) ip 命令详解
ip 命令整合了 ifconfig 与 route 这两个命令，功能更强大。  
**ip 命令的选项**
```
-V：显示指令版本信息
-s：-stats, -statistics 输出更详细的信息；可以使用多个 -s 来显示更多的信息
-f：-family {inet, inet6, link} 强制使用指定的协议族
-4：-family inet 的简写，指定使用的网络层协议是 IPv4 协议
-6：-family inet6 的简写，指定使用的网络层协议是 IPv6 协议
-0：shortcut for -family link
-o：-oneline，输出信息每条记录输出一行，即使内容较多也不换行显示
-r：-resolve，显示主机时，不使用 IP 地址，而使用主机的域名
```
**ip 命令操纵的对象**
```
link ：网卡信息
address：IP 地址信息
neighbour：邻居表
route：路由表
rule：IP 策略
maddress：多播地址
mourte：组播路由缓存条目
tunnel：IP 隧道
```

**查看网络接口信息**
```
ip addr show # 显示所有网络接口的 IP 地址和相关信息。
ip link show # 显示所有网络接口的状态信息。
```
### (8.3) 获取和修改主机名
`hostname` 查看主机名，语法如下: `hostname 选项 参数` ，选项如下：
```
-a : 显示主机别名
-d : 显示 DNS 域名
-f : 显示 FQDN 名称
-i : 显示主机的 ip 地址
-s : 显示短主机名称，在第一个点处截断
-y : 显示 NIS 域名
```
**修改主机名**
```
# 1、临时修改主机名，即系统重启后失效
用法 : hostname 新主机名
hostname ubuntu_dsc # 临时修改主机名为 ubuntu_dsc

# 2、永久修改主机名
用法 : systemctl set-hostname 主机名
systemctl set-hostname dsc # 永久修改文件名为 dsc
```

### (8.4) route 命令，观察路由表信息。
在终端输入 route 命令，结果类似下方。
```
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
default         DSC.mshome.net  0.0.0.0         UG    600    0        0 wlan0
default         DSC             0.0.0.0         UG    32766  0        0 l4tbr0
link-local      0.0.0.0         255.255.0.0     U     1000   0        0 docker0
172.17.0.0      0.0.0.0         255.255.0.0     U     0      0        0 docker0
192.168.55.0    0.0.0.0         255.255.255.0   U     0      0        0 l4tbr0
192.168.137.0   0.0.0.0         255.255.255.0   U     600    0        0 wlan0
```
route 命令输出的路由表字段含义如下：

* Destination 目标网络或目标主机（本机的数据要发送的目的地：子网或主机），与Genmask组成一个网段。

* Gateway 网关(如果是默认网关，网关的地址必须和自己的主机上的其中一块网卡在同一子网)即网关地址。如果没有就显示星号。

* Genmask 网络掩，如果目标网络的的子网掩码为 255.255.255.255,说明目标是一台主机；如果子网掩码为’0.0.0.0’ 说明该路由是默认路由。

* Metric 距离、跳数。暂无用。与目标的""距离""（通常以跳数计算）。

* Use 该路由被使用的次数，可以粗略估计通向指定网络地址的网络流量。

**添加路由**
```
route add [-net|-host] [网域或主机] netmask [mask] [gw|dev]
route del [-net|-host] [网域或主机] netmask [mask] [gw|dev]
参数：
-net ：表示后面接的路由为一个网域（网段）的路由；
-host ：表示后面接的为连接到单部主机的路由；
netmask ：掩码，决定了网域的大小（配合 -net 使用，构成一个网段）；
gw ：gateway 的简写，后续接的是 IP （必须和本机的其中一块网卡处于同一网段），与 dev 不同；
dev ：如果只是要指定由哪一块网卡连线出去，则使用这个设定，后面接 eth0 、eth1 等
```

**删除路由**
```
格式：
route del -net {NETWORK-ADDRESS} netmask {NETMASK} reject
```
### (8.5) ping 测试网络连接 
linux 下的 ping 和 windows 下的 ping 稍有区别, linux 下 ping 不会自动终止,需要按 ctrl+c 终止或者用参数 -c 指定要求完成的回应次数。

1.命令格式：
ping [参数] [主机名或IP地址]

2.命令功能：
ping 命令用于：确定网络和各外部主机的状态；跟踪和隔离硬件和软件问题；测试、评估和管理网络。  
如果主机正在运行并连在网上，它就对回送信号进行响应。  
每个回送信号请求包含一个网际协议（IP）和 ICMP 头，后面紧跟一个 tim 结构，以及来填写这个信息包的足够的字节。缺省情况是连续发送回送信号请求直到接收到中断信号（Ctrl-C）。

ping 命令每秒发送一个数据报并且为每个接收到的响应打印一行输出。  
ping 命令计算信号往返时间和(信息)包丢失情况的统计信息，并且在完成之后显示一个简要总结。ping 命令在程序超时或当接收到 SIGINT 信号时结束。  
Host 参数或者是一个有效的主机名或者是因特网地址。