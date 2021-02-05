import asyncio

"""
代码说明：
1、创建一个列表，列表中有 3 个协程对象，协程内部分别阻塞 1 - 3 秒
2、程序运行过程中，快捷键 Ctrl + C 会触发 KeyboardInterrupt 异常。捕获这个异常，在程序终止前完成 # 3 和 # 4 代码的执行
3、事件循环的 stop 方法取消所有未完成的任务，停止事件循环
4、关闭事件循环
"""


async def work(id, t):
    print('Working...')
    await asyncio.sleep(t)
    print('Work {} done'.format(id))


def main():
    loop = asyncio.get_event_loop()
    coroutines = [work(i, i) for i in range(1, 4)]  # 1
    try:
        loop.run_until_complete(asyncio.gather(*coroutines))  # 2
    except KeyboardInterrupt:
        loop.stop()  # 3
    finally:
        loop.close()  # 4


if __name__ == '__main__':
    main()
