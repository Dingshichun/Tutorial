#!/bin/bash
# the first line must specify a parser

:<<!
date
whoami
echo "please  input your name : "
read name
channel="love"
echo "${name},welcome our channel : ${channel} ! "
!

:<<!
# guess number
num=$( shuf -i 1-22 -n 1 )

while true 
do
echo "please input a number between 1-22:"
read guess
if [ ${guess} -eq ${num} ]; then
    echo "your guess right,do you want to play again ? (y/n)"
    read choice
    if [ ${choice} = "y" ] || [ ${choice} = "Y" ]; then
        num=$( shuf -i 1-22 -n 1 )
        continue
    else
        break
    fi
elif [ ${guess} -lt ${num} ]; then
    echo "your number is lower"
else
    echo "your number is greater"
fi
done
!

:<<!
echo "the first parameter is : $1"
echo "the second parameter is : $2"
echo "all parameter is : $*"
echo "all parameter is : \"$*\"" # "$*" 将所有参数连接成一个字符串整体
echo "all parameter is : $@"
echo "all parameter is : \"$@\""  # "$@" 是所有参数对应的字符串组成的字符串参数列表
echo " have $# paraeters" # "$#" 获取参数个数
for para in "$*"
do
    echo ${para}
done

for para in "$@"
do
    echo ${para}
done
!

:<<!
array1=(1 2 3 4 5)
for arr in ${array1[*]}
do
    echo ${arr}
done
echo "array1 have ${#array1[*]} elements"

array2=([0]=11 [1]=22 [2]=33 [3]=44)
for arr in ${array2[*]}
do
    echo ${arr}
done
echo "array2 have ${#array2[*]} elements"
!

:<<!
res=$((1+2))
echo ${res}

if [ ${val1} -le ${val2} ];then
    echo "val1 is lower equal val2"
else
    echo "val1 is greater than val2"
fi

if [ ${val1} -ge ${val2} ];then
    echo "val1 is greater equal val2"
else 
    echo "val1 is lower than val2"
fi

if [ ${val1} -a ${val2} ];then 
    echo "result is true"
else
    echo "result is false"
fi

if [ ${val1} -o ${val2} ];then
    echo "val1 or val2 is true"
else
    echo "val1 and val2 is false"
fi

if [ ${val1} != ${val2} ];then
    echo "val1 is not equal to val2"
fi

if [[ ${val1} -lt 25 && ${val2} -gt 25 ]];then
    echo "result is true"
fi

num1=34
num2=55
let num1++
let num2--
echo ${num1}
echo ${num2}

num3=43
num4=57
num3=$((num3*3))
num4=$((num4/3))
echo ${num3}
echo ${num4}

num5=99
num6=88
((num5++))
((num6--))
echo ${num5}
echo ${num6}
!

:<<!
file="./run.sh"
if [ -f ${file} ]
then
    echo "this file is general file"
fi

if [ -r ${file} ] && [ -w ${file} ] && [ -x ${file} ]
then
    echo "this file can read、write and execute"
fi
!

:<<!
# define function
function print_name()
{
    echo "please input your name"
    read name
    echo "your name is : ${name}"
}
print_name

print_grade()
{
    echo "please input your grade: "
    read grade
    echo "your grade is : ${grade}"
}
print_grade

function return_value()
{
    echo "input a number"
    read num
    return ${num}
}
return_value
echo $?
!

:<<!
# test 测试整数
num1=33
num2=44
if test ${num1} -eq ${num2}
then
    echo "num1 = num2"
else
    echo "num1 != num2"
fi

# test 测试字符
char1="dsc"
char2="dsl"
if test ${char1} = ${char2}
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
!

:<<!
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

num1=99
while [ ${num1} -gt 33 ]
do
    read -p "input a number that lower equal 33 can break : " num1
done

array=([0]=1 [1]=2 [2]=3 [3]= 4)
for arr in ${array[*]}
do
    echo ${arr}
done

for num in {1..4} # 1 开始，4 结束，必须是整数，两个点也必须要，默认步长为 1
do
    echo ${num}
done

for ((i=1;i<=4;i++)) # 和 c++ 类似，i++ 也可以换成其它步长
do
    echo ${i}
done
!

:<<!
echo "please choose your hobby "
select hobby in "basketball" "pingpong" "soccer ball" "run"
do
    echo "your hobby is : ${hobby}"
    break
done

echo "choose your grade :"
grade_list=(100 99 88 60 44)
select grade in ${grade_list[*]}
do
    echo "your grade is : ${grade}"
    break 
done

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
        *)
            echo "输入错误，重新输入"
            break
            ;;
    esac
done

echo "choose your hobby "
select hobby in "coding" "run" "play"
do
    case ${hobby} in
        "coding")
            echo "coding coding"
            break
            ;;
        "run")
            echo "run run"
            break
            ;;
        "play")
            echo "play play"
            break
            ;;
        *)
            echo "input again"
            break
            ;;
    esac
done
!

:<<!
# 批量创建文件
read -t 30 -p "请输入创建文件的数量 : " num
test=$(echo ${num} | sed 's/[0-9]//g') # 将输入的 num 中的数字全部替换为空格，用于检测输入的是不是数字
if [ -n $n -a -z ${test} ]
then
    [ ! -d ./temp ] && mkdir -p ./temp
    for((i=0;i<${num};i++))
    do
        name=$(date +%N)
        touch ./temp/${name}
        echo "创建 ${name} 成功 ! "
    done
else
    echo "创建失败"
    exit 1
fi

filenames=$(ls ./temp)
number=1
for name in ${filenames}
do
    printf "old name is:%s" ${name}
    new_name=${name}"-"${number}
    rename ${name} ${new_name} ./temp/*
    let number++
    echo -e "new name is : ${new_name}\n"
done
!

:<<!
user_list=$(cat test.txt)
for user in ${user_list}
do
    sudo useradd ${user}
    echo "987654" | sudo passwd --stdin $user &>/dev/null
    [ $? -eq 0 ] && echo " ${user} 用户名和密码添加初始化成功"
done

count=0
for i in 192.169.56.{1..254}
do
    receive=$(ping ${i} -c 2 | awk 'NR==6 {print $4}')
    if [ ${receive} -gt 0 ]
    then
        echo "${i} online"
        let count++
    else
        echo "${i} not online"
    fi
done
echo "在线服务器的个数为：${count}"
!

:<<!
function print_name()
{
    echo "your name is : $1"
    echo "your grade is : $2"
}
print_name dsc 99

print()
{
    echo "your name is : $1"
    echo "have $# parameters"
}
print dsc

function return_val()
{
    read -t 30 -p "please input a number: " num
    return ${num}
}
return_val
echo "input number is : $?"
!

