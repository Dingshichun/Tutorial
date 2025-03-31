# Shell 脚本编程

## (1) shell 基础 
### (1.1) shell 简介
shell 是脚本语言，可直接使用操作系统内核运行。  
shell 的解析器包括 sh,bash,rbash,dash 等，bash 较常用。
shell 预定义了一些系统变量，HOME 表示家目录，PATH 表示环境变量  
$SHELL 表示系统的 shell 版本，一般是 bash，$0 表示当前使用的 shell 版本  
`shell 脚本后缀名为 sh ，脚本的第一行必须指定解析器，比如：#!/bin/bash`

1. shell 脚本的运行方式  
* 语法 1 ：sh 脚本名。利用 sh 命令执行脚本文件，本质是使用 shell 解析器运行脚本文件，不要求脚本文件具有可执行权限。

* 语法 2 ：bash 脚本名。利用 bash 命令执行脚本文件，本质是使用 shell 解析器运行脚本文件，不要求脚本文件具有可执行权限。

* 语法 3 ：./脚本名。执行当前目录下的脚本，前提是脚本具有可执行权限。
```shell
# shell 中的变量默认为全局变量
# $ 表示取变量的值，用法为 ${变量名}
# echo 表示输出内容
cat /etc/shells # 查看可使用的 shell 脚本
name="dsc"
echo ${name}
```

2. shell 的变量类型
shell 的变量包括系统环境变量、自定义变量和特殊符号变量。set 命令可查查看所有变量。  

* 系统环境变量。是系统提供的共享变量，Linux 系统加载 shell 的配置文件中定义的变量共享给所有 shell 程序使用。  
配置文件包含全局和个人，一般直接对全局配置文件进行操作。

* 自定义变量。包括自定义局部变量、自定义常量和自定义全局变量。**定义变量时等号两侧不能有空格**。`unset 变量名` 表示删除变量。  
`readonly 变量名` 表示定义常量（值不可修改）。  
`export 变量名` 表示定义全局变量，当前脚本文件中和子 shell 环境可以使用的变量。  

* 特殊符号变量。
```shell
# (1) $n
# $0 表示获取当前脚本文件名称，$1 ~ ${10} 表示获取第 1~10 个参数。

# (2) $#
# $# 表示输出传入的参数个数

# (3) $* 和 $@
# 两个都是获取所有传入的参数，以便输出所有传入的参数
# 有、无双引号括起来的结果不一样
# 没有双引号时都输出 $1,$2,……,$n
# 有双引号时 "$*" 输出 "$1 $2 …… $n" ，是一个字符串整体
# 有双引号时 "$@" 输出 "$1" "$2"…… "$n" ，是 n 个字符串组成的参数列表

# (4) $? 和 $$
# $? 用于获取上一个 shell 命令的返回码
# 任意一个 shell 命令执行后都有返回码， 0 表示 shell 命令执行成功，非 0 则表示执行失败。

# $$ 用于获取当前 shell 环境的进程 id
```

### (1.2) shell 字符串和数组
1. 字符串的三种格式
* 单引号中的字符串。单引号中的字符串会原样输出，不能解析其中变量的值。
* 双引号中的字符串，推荐使用。可以解析其中的变量值。
* 无引号的字符串。可以解析变量值，但是不能有空格，空格后的内容会被视为其它命令进行解析。但是实践之后发现可以正常输出，不知道原因。
```shell
num=32
echo 'num is:${num}' # 输出：num is:${num}
echo "num is:${num}" # 输出：num is:32
echo numis${num}     # 输出：numis32

# ${#字符串变量名} 获取字符串的长度
name="dsc"
echo ${#name} # 输出：3

# 字符串拼接，推荐使用双引号方式，
str1="your name is : "
str2="dsc"
str="${str1}${str2}"
echo ${str} # 输出：your name is : dsc
```

2. shell 数组
```shell
# shell 数组的定义
# 方式 1 ：array_name=(item1 item2 …… itemN)
# 方式 2 ：([索引下标1]=item1 [索引下标2]=item2 …… [索引下标N]=itemN) 注意索引从 0 开始
array1=(1 2 3 4)
array2=([0]=1 [1]=2 [2]=3 [3]=4)
echo ${#array1[*]} # 获取数组长度
echo ${#array1[@]} # 获取数组长度

# 数组索引
echo ${array1[0]} # 输出：1
for arr in ${array1[*]} # 遍历数组，array1[*] 或 array1[@] 获取数组所有元素
do
    echo ${arr}
done

# unset 删除数组或数组元素
arr1=(22 33 44 55)
unset arr1[0] # 删除第一个元素 22
echo ${arr1[*]} # 输出：33 44 55
unset arr1 # 删除数组 arr1
echo ${arr1[*]} # 输出为空
```

### (1.3)shell 内置命令
```shell
# 1、alias 设置命令别名
# 用法：alias 别名="命令"
# 删除所有别名：unset 别名 -a

# 2、echo 输出信息到标准输出台，默认会在末尾换行
echo "hello world" # 末尾换行
echo -n "hello world" # -n 表示末尾不换行

# "\n" 是换行符
echo "hello \nworld" # 输出：hello \nworld 。因为默认的 echo 无法解析 \n 转义字符
echo -e "hello \nworld" # -e 用于解析转义字符，输出:第一行 hello ，第二行 world

# 3、read ，从终端读取数据
# read 如未指定输入数据保存在哪个变量中，默认保存在 REPLY 中，且 REPLY 只保存最后一个读入命令的数据
read # 执行后等待终端输入数据，假如终端输入 22 33
read # 执行后等待终端输入数据，假如终端输入 44 55
echo ${REPLY} # 上面有两次 read ，REPLY 只保存最后一个 read 读取的内容，即 44 55

read num # 将终端输入的数据保存在变量 num 中
read -p "please input your grade :" grade # -p 即 prompt（提示），打印提示信息

# 4、test ，检查某个条件是否成立，可对整数、字符和文件进行测试
# 对整数的比较
num1=33
num2=44
if test ${num1} -eq ${num2}
then
    echo "num1 = num2"
else
    echo "num1 != num2"
fi
# 对字符的比较
char1="dsc"
char2="dsl"
if test ${char1} = ${char2} # 字符串比较是否相等是用 "=" 
then
    echo "char1 and char2 is same"
else
    echo "char1 and char2 is not same"
fi

# 测试文件
file1="./test.txt"
file2="./CMakeLists.txt"
if test -e ${file1} # -e 检查文件是否存在
then
    echo "file1 exist"
else
    echo "file1 not exist"
fi
```

### (1.4) shell 运算符
1. 算术运算符
```shell
# expr(evaluation expressions)，即求值表达式，可以实现整数计算。
# +, -, \*, /, %, ==, != ，*(乘)要有转义字符
expr 1 + 3 # 输出：4 ，注意 "+" 两侧必须有空格
result=`expr 1 + 3` # 将 1 + 3 的结果赋给 result，不是单引号，是 esc 键下方的 "`"
echo ${result} # 输出：4

# 对变量的操作类似
var1=3
var2=4
expr ${var1} + ${var2} # 输出：7
add=`expr ${var1} + ${var2}` # 两数和的结果赋给 add
echo ${add} # 输出：7
```

2. 比较运算符
```shell
# -eq(equal)、-ne(not equal)、-gt(greater than)、
# -lt(lower than)、-ge(greater equal)、-le(lower equal)
num1=12
num2=22
if [ ${num1} -lt ${num2} ] # 注意 if 语句中的空格
then
    echo "num1 is lower than num2"
else
    echo "num1 greater equal num2"
fi
```

3. 布尔运算符
```shell
# !(非运算) -o(or,或运算) -a(add,与运算)
bool1=88
bool2=33
if [ ${bool1} -a ${bool2} ]
then
    echo "result is true"
fi

if [ ${bool1} != ${bool2} ];then
    echo "bool1 is not equal to bool2"
fi
```

4、逻辑运算符
```shell
# &&(逻辑 AND)、 ||(逻辑 OR)，注意是两个逻辑的结果进行比较
logic1=22
logic2=33
if [[ ${logic1} -lt 25 && ${logic2} -gt 25 ]] # 注意是两个方括号
then
    echo "true"
fi
```

5、自增和自减操作符
```shell
# let 、 $(()) 和 (())

# let 允许对整数实现操作
num1=3
num2=6
let num1++ # 相当于：num1=num1 + 1
let num2-- # 相当于：num2=num2 - 1
echo ${num1} # 输出:4
echo ${num2} # 输出:5

# $(())
num3=8
num4=2
num3=$((num3 - 1))
num4=$((num4 + 1))
echo ${num3} # 输出：7
echo ${num4} # 输出：3

# (())
num5=32
num6=66
((num5++))
((num6--))
echo ${num5} # 输出：33
echo ${num6} # 输出：65
```

6、文件测试运算符
```shell
# 用于检测 Unix 文件的各种属性
# 常见的：-b(检测是否是块设备文件 block)、-c(char)、-d(directory)、-f(普通文件)
# -rwx(分别对应是否可 read、write、execute)
file="./hello.sh"
if [ -f ${file} ] # 注意条件中的空格
then
    echo "it is normal file"
fi

if [ -r ${file} ] && [ -w ${file} ] && [ -x ${file} ]
then
    echo "it can be read、write and execute"
fi
```

### (1.5) shell 函数
```shell
# 定义：function 函数名() { 函数内容 } 或 函数名() { 函数内容 }
# 要传入参数只需要在调用时在函数名后加入参数即可，定义时不需要。
# $1~$9,${10},……,${n} 是传入的第 1~n 个参数。
function print_name()
{
    echo "your name is : $1"
    echo "your grade is : $2"
}
print_name dsc 99 # 调用函数，传入两个参数

print_name()
{
    echo "your name is : $1"
}
print_name dsc # 调用函数，传递一个参数

# 使用 return 返回值，return 只能返回 0~255 之间的整数，其它返回值可直接使用 echo 
function return_val()
{
    echo "please input a number between 0~255 : "
    read num
    return ${num}
}
return_val # 调用函数
echo "you inputed $? !" # 函数返回值在调用该函数后通过 $? 来获得
```

### (1.6) 输入输出重定向
大多数 UNIX 系统命令从你的终端接受输入并将所产生的输出发送回​​到您的终端。  
一个命令通常从一个叫标准输入的地方读取输入，默认情况下，这恰好是你的终端。  
同样，一个命令通常将其输出写入到标准输出，默认情况下，这也是你的终端。
即，输入输出默认都是终端。重定向就是从其它地方输入或输出到其它地方，比如文件。
```shell
# 常用重定向定义
command > file # 将输出重定向到 file ，即将内容以覆盖原内容的方式输出到 file
command >> file # 将输出以追加到原内容末尾的方式输出到 file
command < file # 将输入重定向到 file ，即从 file 接受输入

# 例子
whoami > user.txt # 将 whoami 命令执行的结果输出到 user.txt 文件中，会覆盖文件中原来的内容。
echo "my name is dsc" >> my_name.txt # 将 my name is dsc 追加到 my_name.txt 中

# 假如文件 name.txt 的内容为："hello shell"
grep "shell" < name.txt # 使用 grep 查找 "shell" ，在 name.txt 中查找
wc -l < name.txt # 统计文件 name.txt 的行数，输出：1
```

### (1.7) 包含文件
和其他语言一样， Shell 也可以包含外部脚本。这样可以很方便的封装一些公用的代码作为一个独立的文件。
```shell
# 包含方式有两种
# 方式 1 ：. filename
# 方式 2 ：source filename
# 要在 name3.sh 中包含 name1.sh 和 name2.sh

# name3.sh
#!/bin/bash
. name1.sh # 包含 name1.sh
source name2.sh # 包含 name2.sh
```

### (1.8) 流程控制
包括 if else 语句、while 循环、for 循环、case 等。
```shell
# 1、if 语句
num=88
if [ ${num} -eq 99 ]
then
    echo "num = 99"
elif [ ${num} -eq 77 ]
then
    echo "num = 77"
else
    echo "don"t know"
fi

# 2、case
read -p "input a number between 1~4 :" num
case ${num} in
1)
    echo "number is : ${num}"
    ;;
2)
    echo "number is : ${num}"
    ;;
3)
    echo "number is : ${num}"
    ;;
4)
    echo "number is : ${num}"
    ;; 
*) # "*" 是默认情况，其它条件都不满足时执行
    echo "number is : ${num}"
    ;;   
esac 

# 3、while 循环
# 一行写法：while 条件; do 命令; done
num1=99
while [ ${num1} -gt 33 ] # -gt is greater than
do
    read -p "input a number that lower equal 33 can break : " num1
done

# 4、for 循环
# 方式 1
array=([0]=1, [1]=2, [2]=3, [3]= 4) # 生成一个数组
for arr in ${array[*]} # array[*] 和 array[@] 可以取数组所有元素
do
    echo ${arr}
done
# 方式 2
for num in {1..4} # 1 开始，4 结束，必须是整数，两个点也必须要，默认步长为 1
do
    echo ${num}
done
# 方式 3
for ((i=1;i<=4;i++)) # 和 c++ 类似，i++ 也可以换成其它步长
do
    echo ${i}
done

# 5、select 循环，是无限循环，遇到 break 才会退出，可以和终端进行交互，shell 独有。
# 方式 1
echo "please choose your hobby "
select hobby in "basketball" "pingpong" "soccer ball" "run"
do
    echo "your hobby is : ${hobby}"
    break # 注意 select 是无限循环，使用 break 退出
done
# select 运行结果为下面注释部分
:<<!
please choose your hobby 
1) basketball
2) pingpong
3) soccer ball
4) run
#? 1
your hobby is : basketball
!

# 选择成绩
echo "choose your grade :"
grade_list=(100 99 88 60 44) # 列表
select grade in ${grade_list[*]} # grade[*] 和 grade[@] 取列表中的所有元素
do
    echo "your grade is : ${grade}"
    break # 记得使用 break 退出
done

# 方式 2 ，搭配 case 使用
select hobby in "coding" "basketball" "running" "golf"
do
    case ${hobby} in
        "coding")
            echo "多编程"
            break
            ;;
        "basketball")
            echo "多打篮球"
            break
            ;;
        "running")
            echo "多跑步"
            break
            ;;
        "golf")
            echo "多打高尔夫"
            break
            ;;
        *) # "*)" 表示其它条件都不成立则执行该语句
            echo "输入错误，重新输入"
            break
            ;;
    esac
done
```
### (1.9) 系统函数
```shell
# system predefined functions

# basename 函数根据所给路径提取出文件名
basename ./test.txt # 输出： test.txt
basename ./test.txt .txt # 输出：test 。".txt" 表示删除该后缀名

# dirname 函数，给一个绝对路径，返回文件名之前的前缀路径
dirname /home/dsc/name.txt # 输出：/home/dsc
dirname /home/app/wechat.exe # 输出：/home/app
```

## (2) shell 工具
### (2.1) cut 根据列、字符和字节进行切割、提取
```shell
# 用法：cut [options] filename
# options 包括 -f(列号，获取哪些列)、-d(自定义分割符)、-c(以字符为单位分割)、-b(以字节为单位分割，多字节的字符会分割失败，展示奇怪的结果)、-n(和 -b 连用，表示不分割多字节字符)
cut -d " " test.txt -f 1-4 # 表示以空格符分割文件 test.txt ，并获取第 1-4 列的内容
cut -d " " test.txt -f 1- # 表示以空格符分割文件 test.txt ，并获取第 1 列以后的内容

# linux 中一个英文字母一个字节，一个汉字 3 字节
echo "abc传奇" | cut -b 1-4 # 输出：abc�
echo "abc传奇" | cut -b 1-6 # 输出：abc传
echo "abc传奇" | cut -nb 1-4 # 输出：abc�。按道理说应该会截断，只输出 abc，但是在Windows 上安装的 linux 就是这样输出。

# 查找某个单词，使用 grep 进行查找，会返回包含该单词的所有行，然后再使用 cut 对行内容进行切割即可
echo "your name is dsc" | grep dsc | cut -d " " -f 4 # 输出：dsc
echo -e "her name is anna,\nshe is beautiful !" | grep beautiful | cut -d " " -f 3 # -e 选项是开启转义字符 "\n"，不然无法识别。所以 echo 输出的就是两行内容。

# 输出 bash 进程 id ，ps -aux 查询进程
ps -aux | grep bash | head -n 3 | cut -d " " -f 10-12 # 注意这里以一个空格分割，有多个连续的空格也只是以一个分割，后面的空格会被分割为内容。
```

### (2.2) sed(stream editor,流编辑器)
**sed 是非交互式文本编辑器，vim 则是交互式**。可对文本文件的每一行数据匹配查询之后进行增、删、查、改，适合大文件编辑。  
sed 一次处理一行内容，将一行内容放入缓存之后再进行处理，处理完后将缓存区内容发送到终端。  
**选项**：-i(直接对源文件修改，没有该选项时只是预览)、-f(指定保存路径)、-n(取消默认输出，只输出处理过的行)  
**命令**：a(add，在所匹配的行后面添加)、c(change)、d(delete)、i(insert，在所匹配的行前面插入)、p(print)、s(subtitute,替换)、=(打印被匹配行的行号)、n(读取下一行)
* 添加数据
```shell
# 以修改源文件的方式在 test.txt 文件第三行的后面添加内容 welcome，3a 即第三行后 add
sed -i '3awelcome' test.txt # 注意使用的是单引号

# 以修改源文件的方式将 test.txt 文件的第三行修改为 dsc welcome
sed -i '3cdsc welcome' test.txt

# 以预览的方式在指定内容前面一行（insert）或后面一行（add）插入数据
sed '/dsc/ihandsome' test.txt # test.txt 文件中包含 dsc 的行前面插入 handsome
sed '/dsc/ahandsome' # test.txt 文件中包含 dsc 的行后面插入 handsome

# 以修改源文件的方式在指定内容前、后插入
sed -i '/dsc/ihandsome' test.txt
sed -i '/dsc/ahandsome' test.txt

# 向文件的最后一行前或后添加数据，$ 是最后一行， ^ 是第一行
sed -i '$ait is the end' test.txt # 向最后一行之后添加数据，add
sed -i '$iit is the end' text.txt # 向最后一行之前添加数据，insert
```
* 删除数据
```shell
# 以修改源文件的方式删除 test.txt 的第二行数据
sed -i '2d' test.txt 

# 删除指定范围内的多行数据
sed -i '1,3d' test.txt # 删除 1 到 3 行的数据
sed -i '1,5!d' test.txt # 删除除了 1 到 5 行意外的数据，！ 就是取反
sed -i '$d' test.txt # 删除最后一行
sed -i '/dsc/d' test.txt # 删除包含 dsc 的行
sed -i '/dsc/!d' test.txt # 删除不包含 dsc 的行，! 表示取反
```

* 修改数据
```shell
# 修改数据命令是 c(change)
sed -i '1cfirst' test.txt # 把 test.txt 的第一行修改为 first
sed -i '/usa/cAmerican' test.txt # 将 test.txt 中包含 usa 的整行修改为 American 
```

* 替换数据 s(subtitute)，默认只替换所匹配的第一行的第一个内容，
```shell
sed -i 's/hello/hi/' test.txt # 将所有包含 hello 的行中的第一行的第一个 hello 替换为 hi ，注意 / 的数量 
sed -i 's/hello/hi/g' # g 表示全局替换，所有匹配项都替换。

# 每行末尾拼接一个单词 test
sed -i 's/$/& test/' test.txt # s 是替换，& 是拼接，注意 test 后接 /

# 每行行首添加一个 # 
sed -i 's/^/& #/' test.txt # ^ 表示行首
```

* 其它操作
```shell
# 1、查询
sed -n '/dsc/p' test.txt # 查询 dsc ，并使用 p(print) 打印，-n 只显示查询到的内容

# 从管道接收数据进行查询
ps -aux | sed -n '/sshd/p' # 查询包含 sshd 的进程
ps -aux | grep sshd # grep 查询

# 2、多个命令同时执行
# 方式 1 是使用 -e ，表示执行以一个命令
# 删除第一行，并将 dsc 替换为 app
sed -i -e '1d' -e 's/dsc/app/g' test.txt # 在每个命令前都加上 -e

# 方式 2 是使用 ";" 将命令隔开
sed -i '1d;s/dsc/app/g' test.txt
```

### (2.3) awk 工具
```shell
# awk 默认按空格分割每列
# 将三列数据使用 "&" 进行拼接
echo "123 abc dsc" | awk '{print $1"&"$2"&"$3}' # 输出：abc&234&dsc
```

### (2.4) sort 排序
sort 对字符串、数字等进行排序
```shell
# 使用方法：sort [options] 参数
# 常用选项：-n(按照数值大小排序)、-r(反序)、-t(指定排序时的分隔字符)、-k(指定需要排序的列)、-o(指定文件，将排序后的结果存入)

# -t 指定分割符，-k 指定排序的列，2,2 指的是第二列到第二列，也就是第二列，不能只写一个 2 。
# 2n,2 中间的 n 指的是按数值排序
sort -t " " -k2n,2 sort.txt # 将 sort.txt 按空格分割后的第二列按照数值大小排序。
sort -t " " -k2n,2 -o sort2.txt sort.txt #  -o 将排序后的结果保存到 sort2.txt 中
sort -t " " -k2nr,2 -o sort2.txt sort.txt # 加上 r 表示降序排序

# 多列排序
# 对多少列排序就用多少个 -k 选项，第一个 -k 对第一列字符串升序排序， 第二个 -k 则是对第三列数值内容降序排序
sort -t "," -k1,1 -k3nr,3 sort.txt 
```

### (2.5) 常见面试题
```shell
# 1、查找空行
awk '/^$/{print NR}' test.txt # ^ 代表首行，$ 代表末行，查找首行到末行的空行，并打印行号。

# 2、求一列数据的和
awk '{sum+=$2} END{print "求和："sum}' sort.txt # 求 sort.txt 第二列的和，并打印结果。

# 3、检查文件是否存在，-e 选项检查文件是否存在。
if [ -e ./run.sh ]
then
    echo "exist"
else
    echo "not exist"
fi

# 4、对文件中的一列数据排序，输出每个数据以及求和结果
sort -n sort.txt | awk '{sum+=$1; print $1} END{print "求和："sum}' 

# 5、搜索指定目录下包含某些内容的文件
# 两个管道符将命令分为三个部分：搜索、切割、排序
grep -r "hello" ./ | cut -d ":" -f 1 | sort -u

# 6、批量创建文件
read -t 30 -p "请输入创建文件的数量：" num
test=$( echo ${num} | sed 's/[0-9]//g' ) # 将输入的数字全部替换为空，用于检测输入是否是正确的数字，注意是括号，不是大括号。
if [ -n $n -a -z ${test} ] # 如果 test 为空，说明输入的全是数字
then
    [ ! -d ./temp ] && mkdir -p ./temp # 如果 ./temp 文件夹不存在就创建一个，用于存放文件
    for((i=0;i<${num};i++)) # 循环创建文件
    do
        name=$(date +%N) # 以纳秒取名，注意是括号
        touch ./temp/${name} # 创建文件
        echo "创建 ${name} 成功 ！"
    done
else
    echo "创建失败"
    exit 1
fi

# 7、批量更改文件名
filenames=$(ls ./temp) # 获取某文件夹下的所有文件名
number=1
for name in filenames # 循环改名
do
    printf "old name is :%s" ${name} # 打印旧名字
    new_name=${name}"-"${number} # 定义新名字
    rename ${name} ${new_name} ./temp/* # 重命名文件
    let number++ # number 加 1
    printf "new name is: %s \n" ${new_name} # 打印新名字
done

# 8、批量创建用户，可能需要 root 权限
user_list=$(cat ./test.txt) # 从文件获取要添加的用户名
for user in ${user_list} # 循环创建用户名
do
    useradd ${user} # 添加用户
    echo "987654" | passwd --stdin ${user} &>/etc/null # 设置密码，并将一些提示信息输出到 /etc/null
    [ $? -eq 0 ] && echo "${user} 用户名和密码添加初始化成功" # $? 返回上一个命令执行的状态码，如果上一个命令执行成功会返回状态码 0 。上一个命令执行成功的话输出一些信息。
done

# 9、筛选符合一定长度的单词
# 筛选出长度大于 3 的单词
echo "i want to play basketball" | awk -F "[ ,.]" '{for(i=1;i<=NF;i++){if(length($i)>3) {print $i}}}'

# 10、扫描网络内存活的主机
# 扫描 192.169.56.1~192.169.56.254 之间的 ip 是否存活，并输出是否在线。
count=0
for i in 192.169.56.{1..254}
do
    receive=$(ping ${i} -c 2 | awk -F 'NR==6{print $4')
    if [ ${receive} -gt 0 ]
    then
        echo "${i} online"
        let count++
    else
        echo "${i} not online"
    fi
done
echo "在线服务器的个数为：${count}"
```