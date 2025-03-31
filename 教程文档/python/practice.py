class dog:
    # 私有成员变量和方法都是以双下划线开头，都只能在类中使用，类对象不能调用
    __heart = None  # 私有成员变量

    # 构造方法，在创建对象时会自动调用
    def __init__(self, name, age):
        self.name = name
        self.age = age

    # 以双下划线开始和结尾的方法都是魔术方法，
    # 常用的有 __init__, __str__, __lt__ 等
    def __str__(self):
        return "name: " + self.name + ", age: " + str(self.age)

    def __lt__(self, otherClass):
        """重载小于号, 用于比较两个对象的大小"""
        return self.age < otherClass.age

    def __gt__(self, otherClass):
        """重载大于号, 用于比较两个对象的大小"""
        return self.age > otherClass.age

    def __le__(self, otherClass):
        """重载小于等于号, 用于比较两个对象的大小"""
        return self.age <= otherClass.age

    def __ge__(self, otherClass):
        """重载大于等于号, 用于比较两个对象的大小"""
        return self.age >= otherClass.age

    def __eq__(self, otherClass):
        """重载等于号, 用于比较两个对象的大小"""
        return self.age == otherClass.age

    def bark(self):
        print("woof woof")

    def hi(self, msg):
        print("hi, I am", self.name, msg)


xiaohei = dog("xiaohei", 3)
xiaohei.bark()
xiaohei.hi("nice to meet you")
print(xiaohei.__str__())
xiaobai = dog("xiaobai", 2)
print(xiaobai.__lt__(xiaohei))
print(xiaobai.__gt__(xiaohei))
xiaobai.__heart = "big"
print(xiaobai.__heart)


class idcard:
    id = "card"
    producer = "china"

    def callback(self):
        print("callback")


class phone:
    id = "phone"
    producer = "america"

    def ring(self):
        print("ring")


class duo(idcard, phone):
    id = "duo"

    def pri(self):
        print(super().id)


duo1 = duo()
duo1.callback()
print(duo1.id)
duo1.pri()

# 类型注解，标明变量的类型
mylist: list = [1, 2, 3]  # mylist 的类型是 list
mytuple: tuple = (1, 2, 3)  # mytuple 的类型是 tuple
mystr: str = "hello"  # mystr 的类型是 str

# 还可以进行详细的类型注解
mylist1: list[int] = [1, 2, 3]  # mylist1 的类型是 list，其中元素的类型是 int
mytuple1: tuple[int] = (1, 2, 3)  # mytuple1 的类型是 tuple，其中元素的类型是 int
mytuple2: tuple[int, str] = (
    1,
    "hello",
)  # mytuple2 的类型是 tuple，第一个元素的类型是 int，第二个元素的类型是 str
mydict: dict[str, int] = {
    "a": 1,
    "b": 2,
}  # mydict 的类型是 dict，key 的类型是 str，value 的类型是 int

print(type(mytuple))


# 对函数参数进行类型注解
def add(a: int, b: int) -> int:
    return a + b


from typing import Union

listA: list[Union[int, str]] = [1, 2, 3, "hello"]
dictA: dict[str, Union[int, str]] = {"a": 1, "b": "hello"}


# 多态，子类继承父类的方法，但是可以重写父类的方法
class animal:
    # 父类中空实现的方法叫做抽象方法，也叫做接口，子类必须实现，否则会报错
    def jiao(self):
        pass


class dog(animal):
    name = None

    def jiao(self):
        print("wangwang")


class cat(animal):
    name = None

    def jiao(self):
        print("miaomiao")


cat1 = cat()
dog1 = dog()
cat1.jiao()
dog1.jiao()


# 以父类作为参数，但是传入子类对象，也会调用子类的方法
def ff(pra: animal):
    pra.jiao()


ff(dog1)


# 闭包
def outer(logo: str):
    def inner(name: str):
        print(f"<{logo}>,{name},<{logo}>")

    return inner


result = outer("python")  # 确定 logo 的值
result("hello")  # 调用 inner 函数，传入 name 的值


def outer1(num1: int):
    def inner1(num2: int):
        nonlocal num1  # 使用 nonlocal 关键字，可以在内部函数中修改外部函数的局部变量
        num1 += num2
        print(num1)

    return inner1


result1 = outer1(10)  # result1 是 inner1 函数
result1(20)


def acount(num: int = 0):
    def atm(money, deposit=True):
        nonlocal num
        if deposit:
            num += money
            print(f"存款成功，余额为{num}")
        else:
            if num >= money:
                num -= money
                print(f"取款成功，余额为{num}")
            else:
                print("余额不足")

    return atm


result = acount(1000)
result(500, True)
result(200, False)
result(1300, False)
result(200, True)
# 使用闭包无需全局变量，可以实现数据的封装，保证数据的安全性。
# 闭包中的内部函数会持续引用外部函数的局部变量，
# 所以外部函数的局部变量不会被销毁，会一直存在内存中，直到内部函数被销毁

"""
# 装饰器，用于在不改变原函数的情况下，增加新的功能，也是一种闭包。
# 比如在函数执行前后打印日志，或者在函数执行前后进行权限验证等
def sleep():
    # 睡眠函数，用于模拟网络请求等耗时操作
    import time
    import random
    print("sleeping...")
    time.sleep(random.randint(2,4))
    
def outer2(func:callable): # callable 表示函数类型是可调用的
    # 装饰器，用于在函数执行前后打印日志
    def inner2():
        print("start")
        func()
        print("end")
    return inner2
result=outer2(sleep) # result 是 inner2 函数
result() # 调用 inner2 函数

# 使用 @ 符号，可以直接在函数上方使用装饰器，是一种语法糖

@outer2
def sleep2():
    import time
    import random
    print("sleeping2...")
    time.sleep(random.randint(2,4))
sleep2() # 相当于 outer2(sleep2)()
"""


# 关于装饰器的练习
def inforOuter(func: callable):
    def inforInner(name: str, age: int):
        print("start")  # 增加的功能：在函数执行前打印日志
        func(name, age)
        print("end")  # 增加的功能：在函数执行后打印日志

    return inforInner


@inforOuter  # 相当于 printInfor=inforOuter(printInfor)
def printInfor(name: str, age: int):
    print(f"name:{name},age:{age}")


printInfor("tom", 20)

# 设计模式，是一种编程套路，是一种解决问题的思路，是一种经验总结
# 常见的设计模式有：单例模式，工厂模式，观察者模式，策略模式等
# 单例模式，保证一个类只有一个实例，并提供一个全局访问点
# 避免了重复创建对象，节省了内存空间

# 在 module.py 中定义了一个类 animal，用于演示单例模式，dog 是 animal 的实例
from python.module1 import dog

dog1 = dog  # dog1 是 dog 的实例
dog2 = dog  # dog2 是 dog 的实例
print(dog1)  # dog1 和 dog2 是同一个实例，所以打印结果相同
print(dog2)

# 工厂模式，用于创建对象，将对象的创建和使用分离，提高了代码的灵活性
class animal:
    pass
class dog(animal):
    pass
class cat(animal):
    pass
class person:
    pass

# 通常情况下，我们会直接创建对象
dog1=dog()
cat1=cat()

# 但是如果大批量创建对象，或者创建对象的过程比较复杂，就可以使用工厂模式
# 而且发生变化时，只需要修改工厂类即可，不需要修改其他代码
# 符合现实世界的模式，比如汽车工厂，生产汽车，不需要关心汽车的具体生产过程

# 创建一个工厂类，用于创建对象
class animalFactory:
    def createAnimal(self, name):
        # 工厂方法，用于创建对象
        if name == "dog":
            return dog()
        elif name == "cat":
            return cat()
        else:
            return person()
factory=animalFactory() # 创建工厂对象
dog11=factory.createAnimal("dog") # 通过工厂对象创建对象
cat11=factory.createAnimal("cat") # 通过工厂对象创建对象

