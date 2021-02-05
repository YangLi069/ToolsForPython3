import functools
import time
import asyncio

"""
代码说明：
1、使用协程装饰器创建协程函数
2、协程函数
3、模拟 IO 操作
4、创建事件循环。每个线程中只能有一个事件循环，get_event_loop 方法会获取当前已经存在的事件循环，如果当前线程中没有，新建一个
5、调用协程函数获取协程对象
6、将协程对象注入到事件循环，协程的运行由事件循环控制。事件循环的 run_until_complete 方法会阻塞运行，直到任务全部完成。协程对象作为 run_until_complete 方法的参数，loop 会自动将协程对象包装成任务来运行。后面我们会讲到多个任务注入事件循环的情况
7、打印程序运行耗时
"""


def one():
    start = time.time()

    # @asyncio.coroutine# 1
    # python3.8使用async def 替代 @asyncio.coroutine
    async def do_some_work():  # 2
        print('Start coroutine')
        time.sleep(0.1)  # 3
        print('This is a coroutine')

    loop = asyncio.get_event_loop()  # 4
    coroutine = do_some_work()  # 5
    loop.run_until_complete(coroutine)  # 6

    end = time.time()
    print('运行耗时：{:.4f}'.format(end - start))  # 7


"""
1、事件循环的 create_task 方法可以创建任务，另外 asyncio.ensure_future 方法也可以创建任务，参数须为协程对象
2、task 是 asyncio.Task 类的实例，为什么要使用协程对象创建任务？因为在这个过程中 asyncio.Task 做了一些工作，包括预激协程、协程运行中遇到某些异常时的处理
3、task 对象的 _state 属性保存当前任务的运行状态，任务的运行状态有 PENDING 和 FINISHED 两种
4、将任务注入事件循环，阻塞运行
loop.run_until_complete(coroutine)->RuntimeError: cannot reuse already awaited coroutine
"""


def two():
    start = time.time()

    # @asyncio.coroutine
    # python3.8使用async def 替代 @asyncio.coroutine
    async def do_some_work():
        print('Start coroutine')
        time.sleep(0.1)
        print('This is a coroutine')

    loop = asyncio.get_event_loop()
    coroutine = do_some_work()
    task = loop.create_task(coroutine)  # 1
    print("task是asyncio.Task的实例?", isinstance(task, asyncio.Task))  # 2
    print("Task 状态", task._state)  # 3
    loop.run_until_complete(coroutine)  # 4

    print("Task 状态", task._state)
    end = time.time()
    print('运行耗时：{:.4f}'.format(end - start))


"""
1、使用 async 关键字替代 asyncio.coroutine 装饰器创建协程函数
2、回调函数，协程终止后需要顺便运行的代码写入这里，回调函数的参数有要求，最后一个位置参数须为 task 对象
3、task 对象的 add_done_callback 方法可以添加回调函数，注意参数必须是回调函数，这个方法不能传入回调函数的参数，这一点需要通过 functools 模块的 partial 方法解决，将回调函数和其参数 name 作为 partial 方法的参数，此方法的返回值就是偏函数，偏函数可作为 task.add_done_callback 方法的参数
"""


def three():
    start = time.time()

    async def corowork():  # 1
        print('Start coroutine')
        time.sleep(0.1)
        print('This is a coroutine')

    def callback(name, task):  # 2
        print("Hello {}".format(name))
        print("Coroutine state: {}".format(task._state))

    loop = asyncio.get_event_loop()
    coroutine = corowork()
    task = loop.create_task(coroutine)
    task.add_done_callback(functools.partial(callback, "Shiyanlou"))  # 3
    loop.run_until_complete(coroutine)

    end = time.time()
    print('运行耗时：{:.4f}'.format(end - start))


"""
代码说明：
1、await 关键字等同于 Python 3.4 中的 yield from 语句，后面接协程对象。asyncio.sleep 方法的返回值为协程对象，这一步为阻塞运行。asyncio.sleep 与 time.sleep 是不同的，前者阻塞当前协程，即 corowork 函数的运行，而 time.sleep 会阻塞整个线程，所以这里必须用前者，阻塞当前协程，CPU 可以在线程内的其它协程中执行
2、协程函数的 return 值可以在协程运行结束后保存到对应的 task 对象的 result 方法中
3、创建两个协程对象，在协程内部分别阻塞 3 秒和 1 秒
4、创建两个任务对象
5、将任务对象作为参数，asyncio.gather 方法创建任务收集器。注意，asyncio.gather 方法中参数的顺序决定了协程的启动顺序
6、将任务收集器作为参数传入事件循环的 run_until_complete 方法，阻塞运行，直到全部任务完成
7、任务结束后，事件循环停止，打印任务的 result 方法返回值，即协程函数的 return 值
到这一步，大家应该可以看得出，上面的代码已经是异步编程的结构了，在事件循环内部，两个协程是交替运行完成的。简单叙述一下程序协程部分的运行过程：
-> 首先运行 task1
-> 打印 [corowork] Start coroutine ONE
-> 遇到 asyncio.sleep 阻塞
-> 释放 CPU 转到 task2 中执行
-> 打印 [corowork] Start coroutine TWO
-> 再次遇到 asyncio.sleep 阻塞
-> 这次没有其它协程可以运行了，只能等阻塞结束
-> task2 的阻塞时间较短，阻塞 1 秒后先结束，打印 [corowork] Stop coroutine TWO
-> 又过了 2 秒，阻塞 3 秒的 task1 也结束了阻塞，打印 [corowork] Stop coroutine ONE
-> 至此两个任务全部完成，事件循环停止
-> 打印两个任务的 result
-> 打印程序运行时间
-> 程序全部结束
"""


def four():
    start = time.time()

    async def corowork(name, t):
        print('Start coroutine', name)
        await asyncio.sleep(t)  # 1
        print('Stop coroutine', name)
        return 'Coroutine {} OK'.format(name)  # 2

    loop = asyncio.get_event_loop()
    coroutine1 = corowork('One', 3)  # 3
    coroutine2 = corowork('Two', 1)  # 3
    task1 = loop.create_task(coroutine1)  # 4
    task2 = loop.create_task(coroutine2)  # 4
    gather = asyncio.gather(task1, task2)  # 5
    loop.run_until_complete(gather)  # 6
    print("Task1 result:", task1.result())  # 7
    print("Task2 result:", task2.result())  # 7

    end = time.time()
    print('运行耗时：{:.4f}'.format(end - start))


# one()
# two()
# three()
four()
