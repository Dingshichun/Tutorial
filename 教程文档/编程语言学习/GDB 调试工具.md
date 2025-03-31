# GDB(GNU debugger) 教程
## (1) GDB 简介
GDB 是 Linux 下非常好用且强大的调试工具。GDB 可以调试 C、C++、Go、java、 objective-c、PHP 等语言。  
GDB 主要完成以下 4 个方面的功能：  
1、按照自定义的方式启动运行需要调试的程序。  
2、可以使用指定位置和条件表达式的方式来设置断点。  
3、程序暂停时的值的监视。  
4、动态改变程序的执行环境。  


## (2) gdb 基础
### (2.1) gdb 运行流程
要使用 gdb 进行调试，需要具有调试信息。要保留调试信息，需要在使用编译器编译源代码时使用 `-g` 参数。比如下面使用 g++ 编译 main.cpp 文件，-g 保留调试信息，-o 指定生成的可执行程序名字为 main
```
g++ -g main.cpp -o main
```

要查看一个可执行文件是否具有调试信息，直接使用 gdb 运行该程序，如：`gdb ./main` 
```
# 如果没有调试信息，会有 "no debugging symbols found" 提示
Reading symbols from /home/minger/share/tencent/gdb/main…(no debugging symbols found)…done.

# 如果有调试信息，会有下面的提示
Reading symbols from /home/minger/share/tencent/gdb/main…done.
```
### (2.2) gdb 基本命令
基本调试命令如下
```
命令 (简写)
help            # 查看 gdb 所有内部命令和使用说明
run (r)         # 重新开始运行调试
start           # 单步执行，运行程序，停在第一执行语句
list (l)        # 查看原代码
set             # 设置变量的值
next (n)        # 单步调试（逐过程：函数直接运行）
step (s)        # 单步调试（逐语句：跳入自定义函数内部执行）
backtrace (bt)  # 查看函数调用的栈帧和层级关系
frame (f)       # 切换函数的栈帧
info (i)        # 查看函数内部局部变量的值
finish          # 结束当前函数，返回到函数调用点
continue (c)    # 继续运行
print (p)       # 打印值和地址
quit (q)        # 退出 gdb
```

### (2.3) gdb 调试
1. 定义源程序 main.cpp
```cpp
// main.cpp 代码
#include<iostream>
using namespace std;

void print()
{
    cout<<"hello world"<<endl;
}
int i = 99; // 全局变量

int main()
{
    print();
    i = 88; // 修改全局变量的值
    cout<<"i 的值是："<<i<<endl;
    return 0;
}
```
2. 生成调试信息
```
# -g 生成调试信息，-o 指定可执行程序名
g++ -g main.cpp -o main
```
有调试信息后即可调试，打开终端，进入可执行程序 main 所在的目录，执行 `gdb ./main` 就会进入 gdb 调试命令行。输入 r 执行调试，因为没有设置断点，会直接执行到程序结束。

3. 执行调试  
**设置断点**。   
格式 1 ：break 行号（或：b 行号 ，或：br 行号）    
格式 2 ：c 或 c++ 文件可以使用文件名和行号，比如：break main.cpp:11 ，就是在 main.cpp 的第 11 行设置断点。    
格式 3 ：break 函数名。比如：break main ，就是在函数处设置断点。    
格式 4 ：条件断点。在指定条件下才有断点，比如：break main.cpp:11 if num>10 ，就是在 num>10 的时候才设置断点。  

**查看断点**：info breakpoints 或 info b 或 info br 
**删除断点**：delete breakpoints 断点编号 或 d 断点编号，比如：delete breakpoints 1 或 d 1 ，就是删除第一个断点。  
**查看代码**：list 或 l ，可以指定行号：list first,end ，比如：list 1,10 ，就是查看 1-10 行的代码。  
还可以查看指定文件中的行或函数，比如：list main.cpp:print ，就是查看 main.cpp 中的 print 函数。比如 list main.cpp:1,9 就是查看 main.cpp 的 1-9 行。

4. 单步调试和查看变量  
**单步调试** ：包括 **逐过程**（不会进入函数内部，直接得到函数的输出）和 **逐语句**（会进入函数内部，将函数内部的每一条语句执行）。
```
# next(n)，用于在程序断住后，继续执行下一条语句，不进入函数内部。
# step(s)，它可以单步跟踪到函数内部。
# continue(c)或者 fg ，它会继续执行程序，直到再次遇到断点处。
```

**查看变量**   
```
格式：print 或 p 变量名。
print num # 打印 num
区分多个函数或多个文件中的同名变量：print 'main.cpp'::num
打印指针指向的内容需要解引用：print *ptr ，如果指针指向数组，则只能打印第一个值，如果要打印全部值，需要使用 @ 并指定打印个数，比如：print *ptr@len ，len 是数组长度
```
5. 设置变量和观察点
**设置变量** ：使用 print 命令查看了变量的值，如果感觉这个值不符合预期，想修改下这个值，再看下执行效果。这种情况下，我们该怎么办呢？通常情况下，我们会修改代码，再重新执行代码。使用 gdb 的 set 命令，一切将变得更简单。
```
方法 1 ：print 变量名=修改值。比如：print num=99 ，就将 num 的值修改为 99 。
方法 2 ：set var 变量名=修改值。var 是告诉调试器这是一个变量，不加上会出错。
注意，修改值要在调试到原值之后的代码处进行才行。比如 c++ 部分代码如下：
num = 99；
cout<<"welcome"<<endl;
cout<<num<<endl;
调试时要进行到 num = 99 代码行后面修改 num 的值才有效，如果在之前修改的话，调试到这里之后 num 的值又变为了 99 ，最后 cout 输出的也是 99 。 
```
**设置观察点** 作用就是：当被观察的变量发生变化后，程序就会暂停执行，并把变量的原值(Old)和新值(New)都会显示出来。设置观察点的命令是 watch 。