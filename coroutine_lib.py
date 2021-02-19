'''
这个程序是一个精简的协程库实现，除了用于演示的应用代码 TcpServer ，整个库也就 100 来行代码！

我们模仿常见协程库，引入 Future ，代表一个在未来才能获取到的数据。Future 一般由协程创建，典型的场景是这样的：协程在等待一个 IO 事件，这时它便创建一个 Future 对象，并把执行权归还给事件循环。

例子中的 Future 类，有 4 个重要的属性：

loop ，当前事件循环对象；
done ，标识目标数据是否就绪；
result ，目标数据；
co ，关联协程，Future 就绪后，事件循环 loop 将把它放入可执行队列重新调度；
注意到，Future 是一个 可等待对象 ( awaitable )，它实现了 __await__ 方法。当数据未就绪时，通过 yield 让出执行权，这时事件循环将协程记录在 Future 中。当数据就绪后，事件循环将协程放回可执行队列重新调度。

协程库还将套接字进行 异步化 封装，抽象出 AsyncSocket 类，接口与原生 socket 对象类似。除了保存原生 socket 对象，它还保存事件循环对象，以便通过事件循环订阅 IO 事件。

create_future_for_events 方法创建一个 Future 对象，来等待一个不知何时发生的 IO 事件。创建完 Future 对象后，进一步调用 loop 相关方法，将感兴趣的 IO 事件注册到 epoll 。当相关事件就绪时，事件循环将执行回调函数 handler ，它解除 epoll 注册，并将活跃事件作为目标数据设置到 Future 上 (注意 set_result 将唤醒协程)。

然后是套接字系列操作函数，以 accept 为例，它不断尝试调用原生套接字，而原生套接字已被设为非阻塞。如果套接字已就绪，accept 将直接返回新连接，协程无须等待。

否则，accept 方法抛出 BlockingIOError 异常。这时，协程调用 create_future_for_events 方法创建一个 Future 订阅读事件 ( EPOLLIN )，并等待事件到达。

recv 、send 方法封装也是类似的，不同的是 send 需要订阅 可写事件 ( EPOLLOUT )。

好了，终于来到协程库了主角事件循环 EventLoop 对象了，它有 3 个重要属性：

epoll ，这是一个 epoll 描述符，用于订阅 IO 事件；
runnables ，可执行协程队列；
handlers ，IO 事件回调处理函数映射表；
register_for_polling 方法注册感兴趣的 IO 事件和处理函数，它以文件描述符为键，将处理函数记录到映射表中，然后调用 epoll 完成事件订阅。unregister_from_polling 方法则刚好相反，用于取消注册。

add_coroutine 将一个可运行的协程加入队列。run_coroutine 则调度一个可执行协程，它调用 send 将执行权交给协程。如果协程执行完毕，它将输出提示；协程需要等待时，会通过 yield 归还执行权并提交 Future 对象，它将协程记录到 Future 上下文。schedule_runnable_coroutines 将可执行协程逐个取出并调度，直到队列为空。

run_forever 是事件循环的主体逻辑，这是一个永久循环。每次循环时，先调度可执行协程；然后通过 poll 等待协程注册的 IO 事件；当有新事件到达时，取出回调函数 handler 函数并调用。

TcpServer 只是一个普通的协程式应用，无须赘述。接下来，我们逐步分析，看看程序启动后都发生什么事情：

创建事件循环 EventLoop 对象，它将创建 epoll 描述符；
创建 TcpServer 对象，它通过事件循环 loop 创建监听套接字，并将 serve_forever 协程放入可执行队列；
事件循环 loop.run_forever 开始执行，它先调度可执行队列；
可执行队列一开始只有一个协程 TcpServer.serve_forever ，它将开始执行 (由 run_coroutine 驱动)；
执行权来到 TcpServer.serve_forever 协程，它调用 AsyncSocket.accept 准备接受一个新连接；
假设原生套接字未就绪，它将抛出 BlockingIOError 异常；
由于 IO 未就绪，协程创建一个 Future 对象，用来等待一个未来的 IO 事件 ( AsyncSocket.accept )；
于此同时，协程调用事件循环 register_for_polling 方法订阅 IO 事件，并注册回调处理函数 handler ；
future 是可以个可等待对象，await future 将执行权交给它的 __await__ 函数；
由于一开始 future 是未就绪的，这时 yield 将协程执行逐层归还给事件循环，future 对象也被同时上报；
执行权回到事件循环，run_coroutine 收到协程上报的 future 后将协程设置进去，以便 future 就绪后重新调度协程；
可执行队列变空后，事件循环开始调用 epoll.poll 等待协程注册的 IO 事件 ( serve_forever )；
当注册事件到达后，事件循环取出回调处理函数并调用；
handler 先将套接字从 epoll 解除注册，然后调用 set_result 将活跃事件作为目标数据记录到 future 中；
set_result 将协程重新放回可执行队列；
IO 事件处理完毕，进入下一次事件循环；
事件循环再次调度可执行队列，这时 TcpServer.serve_forever 协程再次拿到执行权；
TcpServer.serve_forever 协程从 yield 语句恢复执行，开始返回目标数据，也就是先前设置的活跃事件；
AsyncSocket.accept 内 await future 语句取得活跃事件，然后循环继续；
循环再次调用原生套接字，这时它早已就绪，得到一个新套接字，简单包装后作为结果返回给调用者；
TcpServer.serve_forever 拿到代表新连接的套接字后，创建一个 serve_client 协程并交给事件循环 loop ；
TcpServer.serve_forever 进入下一次循环，调用 accept 准备接受下一个客户端连接；
如果监听套接字未就绪，执行权再次回到事件循环；
事件循环接着调度可执行队列里面的协程，*TcpServer.*serve_client 协程也开始执行了；
etc
这看着就像一个精密的机械装置，有条不紊的运行着，环环相扣！
'''

import select

from collections import deque
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR


def create_listen_socket(bind_addr='0.0.0.0', bind_port=55555, backlogs=102400):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind((bind_addr, bind_port))
    sock.listen(backlogs)
    return sock


class Future:

    def __init__(self, loop):
        self.loop = loop
        self.done = False
        self.result = None
        self.co = None

    def set_coroutine(self, co):
        self.co = co

    def set_result(self, result):
        self.done = True
        self.result = result

        if self.co:
            self.loop.add_coroutine(self.co)

    def __await__(self):
        if not self.done:
            yield self
        return self.result


class AsyncSocket:

    def __init__(self, sock, loop):
        sock.setblocking(False)

        self.sock = sock
        self.loop = loop

    def fileno(self):
        return self.sock.fileno()

    def create_future_for_events(self, events):
        future = self.loop.create_future()

        def handler(fileno, active_events):
            self.loop.unregister_from_polling(self.fileno())
            future.set_result(active_events)

        self.loop.register_for_polling(self.fileno(), events, handler)

        return future

    async def accept(self):
        while True:
            try:
                sock, addr = self.sock.accept()
                return AsyncSocket(sock=sock, loop=self.loop), addr
            except BlockingIOError:
                future = self.create_future_for_events(select.EPOLLIN)
                await future

    async def recv(self, bufsize):
        while True:
            try:
                return self.sock.recv(bufsize)
            except BlockingIOError:
                future = self.create_future_for_events(select.EPOLLIN)
                await future

    async def send(self, data):
        while True:
            try:
                return self.sock.send(data)
            except BlockingIOError:
                future = self.create_future_for_events(select.EPOLLOUT)
                await future


class EventLoop:

    def __init__(self):
        self.epoll = select.epoll()

        self.runnables = deque()
        self.handlers = {}

    def create_future(self):
        return Future(loop=self)

    def create_listen_socket(self, bind_addr, bind_port, backlogs=102400):
        sock = create_listen_socket(bind_addr, bind_port, backlogs)
        return AsyncSocket(sock=sock, loop=self)

    def register_for_polling(self, fileno, events, handler):
        print('register fileno={} for events {}'.format(fileno, events))
        self.handlers[fileno] = handler
        self.epoll.register(fileno, events)

    def unregister_from_polling(self, fileno):
        print('unregister fileno={}'.format(fileno))
        self.epoll.unregister(fileno)
        self.handlers.pop(fileno)

    def add_coroutine(self, co):
        self.runnables.append(co)

    def run_coroutine(self, co):
        try:
            future = co.send(None)
            future.set_coroutine(co)
        except StopIteration as e:
            print('coroutine {} stopped'.format(co.__name__))

    def schedule_runnable_coroutines(self):
        while self.runnables:
            self.run_coroutine(co=self.runnables.popleft())

    def run_forever(self):
        while True:
            self.schedule_runnable_coroutines()

            events = self.epoll.poll(1)
            for fileno, event in events:
                handler = self.handlers.get(fileno)
                if handler:
                    handler(fileno, events)


class TcpServer:

    def __init__(self, loop, bind_addr='0.0.0.0', bind_port=55555):
        self.loop = loop
        self.listen_sock = self.loop.create_listen_socket(bind_addr=bind_addr, bind_port=bind_port)
        self.loop.add_coroutine(self.serve_forever())

    async def serve_client(self, sock):
        while True:
            data = await sock.recv(1024)
            if not data:
                print('client disconnected')
                break

            await sock.send(data.upper())

    async def serve_forever(self):
        while True:
            sock, (addr, port) = await self.listen_sock.accept()
            print('client connected addr={} port={}'.format(addr, port))

            self.loop.add_coroutine(self.serve_client(sock))


def main():
    loop = EventLoop()
    server = TcpServer(loop=loop)
    loop.run_forever()


if __name__ == '__main__':
    main()
