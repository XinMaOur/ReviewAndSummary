## 全局解释器锁GIL(Global interpreter lock)
### 1.内存中可以存放多个程序,但被解释器执行的时候只能有一个线程。
    一句话概括: GIL保证了同一时刻只有一个线程在运行。
### 2.在多线程环境中，python虚拟机会已以下方式执行，
    2.1 设置GIL
    2.2 切换到一个线程去执行
    2.3 运行:
        a.指定数量的字节码的指令，或者
        b.线程主动让出控制(可以调用time.sleep())
    2.4 把线程是遏制为睡眠状态
    2.5 解锁GIL
    2.6 重复上述步骤
### 3.话说GIL限制了同一时刻执行的线程数,使python变成了单线程,有什么姿势可以 poke 呢？
    3.1 调用外部代码(如C/C++扩展函数)，GIL将会被锁定,直到这个函数结束为止(由于这期间没有python字节码被运行，所以不会做线程切换)
    3.2 对所有面向IO的(会调用内建的操作系统哦C代码的)程序来说，GIL会在IO调用之前释放，以保证其他的线程在等待IO的时候在运行。

## Tread
    Tread会在主线程结束时，所有的线程都会被强制结束掉,没有警告也没有正常的清楚工作。
## threading模块
    提供了更高级的线程管理功能。
    threading的Thread类是你主要的运行对象。
### eg
    threadingtest.py
    
## Queue模块
    允许用户创建一个多个线程之间共享数据的队列数据结构
### eg
    threading.queue.test.py