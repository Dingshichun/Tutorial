"""
class animal:
    __password = None
    __sex = None
    name = None
    age = None

    def __init__(self, name:str, age:int)->None:
        self.name = name
        self.age = age

    def __str__(self):
        return f"name is:{self.name},age is:{self.age}"

    def __lt__(self, otherClass: object) -> bool:
        return self.age < otherClass.age

    def __gt__(self, otherClass: object) -> bool:
        return self.age > otherClass.age

    def __eq__(self, otherClass: object) -> bool:
        return self.age == otherClass.age

    def __le__(self, otherClass: object) -> bool:
        return self.age <= otherClass.age

    def __ge__(self, otherClass: object) -> bool:
        return self.age >= otherClass.age

    def bark(self)->None:
        print("woof woof")

    def hi(self, msg:str)->None:
        print(f"hi, I am {self.name}, {msg} !")


class animalFactory:
    def creatAnimal(self, name:str, age:int)->animal:
        return animal(name, age)


a1 = animalFactory()
dog1 = a1.creatAnimal("dog1", 3)
dog1.hi("nice to meet you")
dog2=a1.creatAnimal("dog2", 2)
cat1=a1.creatAnimal("cat1", 1)
print(cat1>dog2)

class dog(animal):
    def hi(self, msg):
        return super().hi(msg)
d1=dog("d1", 3)
d1.hi("nice to meet you")

from typing import Union
mylist:list[int]=[1,2,3,4,5]
myNum:list[Union[int,str]]=[1,2,3,4,5,"a","b","c"]
myName:str="hello"
myDict:dict[str,int]={"a":1,"b":2,"c":3}
mydict2:dict[str,Union[int,str]]={"a":1,"b":"b","c":3}

def myfunc(name:str='dsc',age:int=27,grade:float=88)->None:
    print(f"my name is {name},age is {age},grade is {grade}")

myfunc("dsd",22,99)

# 闭包，装饰器也是一种闭包
def outer(func:callable)->callable:
    # 注意闭包的外部函数传入的参数是函数，内部函数传入的参数是函数的参数
    def inner(name:str,age:int)->None:
        import time
        import random
        print("start")
        func(name,age)
        time.sleep(random.randint(1,2))
        print("end")
    return inner

@outer # 装饰器的语法糖，相当于 printInfor=outer(printInfor)
def printInfor(name:str,age:int)->None:
    print(f"name is {name},age is {age}")

# 使用语法糖之后，可以直接调用 printInfor 函数，而不需要再调用 outer 函数
printInfor("dsc",27)

# api key：sk-fb21ec50ee5444ec8828043ca2eb38f6
"""

# 装饰器的简单使用
"""
def hello():
    print("hello world")


a = hello # 函数名可以赋值给变量，变量名可以作为函数名使用
# a() # 通过变量名调用函数，等价于 hello()
# print(a.__name__)
# print(a.__module__)

# 高阶函数，传入函数，返回函数。函数名可以作为参数传入，也可以作为返回值返回。

def high(func)->None:
    print(func)
    func()
high(hello)

def runTime(func):
    def inner(*args, **kwargs):
        # 使用 *args, **kwargs 可以接收任意数量的参数 
        import time
        start = time.time()
        func(*args, **kwargs) # 这里也要使用 *args, **kwargs 来传递参数
        end = time.time()
        print(f"run time is {end-start}")
    return inner # 返回内部函数的函数名，而不是调用内部函数，所以不加括号

@runTime # 装饰器的语法糖，相当于 hello=runTime(hello)
def hi(name:str,age:int): 
    # 函数定义时不需要加 *args, **kwargs，因为装饰器已经帮我们做了    
    print(f"hi,my name is {name},age is {age}")

hi("dsc",27) # 调用 hi() 函数，相当于调用 inner() 函数，inner() 函数中调用了 hi() 函数
"""


"""
# 装饰器带参数，被装饰函数有返回值。
def decrate(*args,**kwargs): 
    print(args)
    print(kwargs)
    def outer(func):  # 这里的 func 就是被装饰的函数 
        def inner(*args, **kwargs):
            print("start")
            res = func(*args, **kwargs) # 这里的 res 接收被装饰函数的返回值
            print("end")
            return res # 返回被装饰函数的返回值 
        return inner  # 返回内部函数的函数名，而不是调用内部函数，所以不加括号
    return outer # 返回外部函数的函数名，而不是调用外部函数，所以不加括号

@decrate("dsc",27) # 装饰器的语法糖，相当于 hello=decrate(*args,**kwargs)(hello)
def hi(name:str,age:int)->str:
    print(f"hi,my name is {name},age is {age}")
    return age # 被装饰函数有返回值
    
print(hi("dsc",27)) # 调用 hi() 函数，相当于调用 inner() 函数，inner() 函数中调用了 hi() 函数
"""

# 迭代器和生成器
from collections.abc import Iterable


class student:
    def __init__(self, stu):
        self.stu = stu

    # 定义 __iter__ 和 __getitem__ 方法，都可使得类的实例对象可以被迭代
    # 但是 __getitem__ 方法的优先级高于 __iter__ 方法
    def __getitem__(self, item):  # 这里的 item 就是 students.__getitem__(i) 中的 i
        return self.stu[item]


students = student(["dsc", "dsff", "dsf"])

for i in students:  # 这里的 i 就是 students.__getitem__(i) 的返回值
    print(i)

a = [2, 3, 4]  # 列表是可迭代对象，但不是迭代器，不能用 next() 函数
a_iter = iter(a)  # 将列表转换为迭代器,迭代器没有 len 属性，不能用 for 循环遍历
print(type(a_iter))
# print(dir(a_iter))
print(next(a_iter))
for item in a_iter:
    print(item)

# 生成器，关键字是 yield
# yield 会将函数变成生成器，生成器是迭代器，
# 可以用 next() 函数，也可以用 for 循环遍历
# yield 和 return 的区别：yield 会将函数变成生成器，生成器是迭代器，
# 可以用 next() 函数，也可以用 for 循环遍历，
# return 会将函数变成普通函数，返回值是 return 后面的值


def demo():
    print("hello")
    res = yield 5
    print("world")
    print(res)


def demo1():
    print("hi")
    return 5


a = demo()  # a 是一个生成器
demo1()  # 直接调用普通函数 demo1()

# print(
#     next(a)
# )  # 打印返回值 5，执行到 yield 5 时，函数暂停，等待下一次调用 next()函数时继续执行

# # 继续执行，打印 world ,但是没有可迭代对象了，会返回 StopIteration 错误，
# # 但是如果在 for 循环中遍历迭代器，会自动解决该问题。
# next(a)

b = demo()
print(next(b))  # 使用 next() 方法预激活生成器，然后才能使用 send() 方法迭代

# 也可以使用 send(None) 方法预激活生成器，只能传入 None 来激活生成器
# send() 方法可以向生成器发送数据，数据会传递给 yield 表达式的结果
# b.send("welcome")

class dog:
    def __new__(cls,*args,**kwargs): # 该魔法方法相当于构造函数
        print("dog 对象被创建了")
        return super().__new__(cls) # 返回一个新的对象, 如果不返回，则不会创建对象
    def __init__(self, name, age): # 该魔法方法相当于初始化方法
        self.name = name
        self.age = age
    def __del__(self): # 该魔法方法相当于析构函数
        print("dog 对象被销毁了")

d = dog("小黑", 2)
del d # 手动销毁对象，会调用 __del__ 方法，如果没有手动销毁，会在程序结束时自动销毁
print("bye bye")
