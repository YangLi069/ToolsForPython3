import asyncio
import functools

"""
call_later 同 loop.call_soon 一样，可将普通函数作为任务放到事件循环里，
不同之处在于此方法可延时执行，第一个参数为延时时间。
运行结果：
[workA]  start
[hello]  Hello, Kitty
[workB]  start
[hello]  Hello, Jerry
[workA]  stop
[hello]  Hello, Tom
[workB]  stop
这五个任务在一个事件循环里是顺序执行，遇到阻塞执行下一个，程序执行顺序如下：
-> 首先执行任务一，打印一行后阻塞 1 秒，执行任务二
-> 任务二是 call_later 1.2 秒，就相当于一个 1.2 秒的 asyncio.sleep
-> 注意，call_later 这个延时 1.2 秒是事件循环启动时就开始计时的
-> 任务二阻塞，执行任务三，这个简单，打印一行就完事儿
-> 接着执行任务四，打印一行后阻塞 2 秒
-> 接着执行任务五，还是 call_later 1 秒，阻塞
-> 以上是五个任务第一轮的执行情况

第二轮开始前，CPU 一直候着，现在还有 4 个任务，任务三已完成
-> 第一个发出执行信号的是任务五，它只阻塞 1 秒
-> 上面已经说了，这个 1 秒是从事件循环启动时开始算
-> 所以这个阻塞肯定比任务一的阻塞 1 秒先结束
-> CPU 执行完任务五，任务一也阻塞结束了，执行之
-> 然后是任务二，最后是任务四
-> 第二轮打印了 4 行，全部任务完成，停止事件循环
"""
def hello(name):  # 普通函数
    print('[hello]  Hello, {}'.format(name))


async def work(t, name):  # 协程函数
    print('[work{}]  start'.format(name))
    await asyncio.sleep(t)
    print('[work{}]  stop'.format(name))


def main():
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(work(1, 'A'))  # 任务 1
    loop.call_later(1.2, hello, 'Tom')  # 任务 2
    loop.call_soon(hello, 'Kitty')  # 任务 3
    task4 = loop.create_task(work(2, 'B'))  # 任务 4
    loop.call_later(1, hello, 'Jerry')  # 任务 5
    loop.run_until_complete(task4)


if __name__ == '__main__':
    main()
