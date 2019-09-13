# 如何在列表、字典和集合中根据条件筛选数据
# 方法1：列表解析、字典解析或者集合解析
from random import randint

l = [randint(-10, 10) for _ in range(10)]
print([x for x in l if x >= 0])

d = {'student%d' % i: randint(50, 100) for i in range(1, 21)}
print({k: v for k, v in d.items() if v >= 90})

s = {randint(0, 20) for _ in range(20)}
print({x for x in s if x % 3 == 0})

# 方法2：filter函数
g = filter(lambda x: x >= 0, l)
print(list(g))

d = filter(lambda item: item[1] >= 90, d.items())
print(dict(d))

