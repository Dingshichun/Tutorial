# 进程和线程
# 进程是程序的一次执行，是系统资源分配的最小单位，进程之间相互独立，互不影响
# 线程是进程的一个执行单元，是 CPU 调度的最小单位，线程之间共享进程的资源，可以实现并发执行
# Python 中的多线程是伪多线程，因为 GIL 锁的存在，同一时刻只有一个线程在执行
# 但是 Python 中的多进程是真正的多进程，因为每个进程都有独立的内存空间，互不影响
# Python 中的多进程和多线程都是通过内置的模块实现的，比如 multiprocessing 模块，threading 模块
# 多进程适合 CPU 密集型任务，多线程适合 IO 密集型任务

import time
import threading

def sing(msg):
    while True:
        print(msg)
        time.sleep(1)
def dance(msg):
    while True:
        print(msg)
        time.sleep(1)
if __name__ == "__main__":
    # sing()
    # dance()
    # 由于这里是单线程，所以 sing() 函数和 dance() 函数是串行执行的
    # sing() 函数执行完之后，dance() 函数才会执行
    # 但是这里 sing() 函数中有一个死循环，所以 dance() 函数永远不会执行
    
    # 使用多线程，可以实现多个任务的并发执行
    # threading.Thread(target=sing,args=("sing a song",)).start() # 创建一个线程，执行 sing() 函数
    # threading.Thread(target=dance,kwargs={"msg":"dance"}).start() # 创建一个线程，执行 dance() 函数
    pass