# 从多个字典中找出公共键
# 方法1：从第一个字典中取每个键在其他字典中依次查找是否存在
from random import randint, sample

d1 = {k: randint(1, 3) for k in sample('abcdefgh', randint(3, 6))}
d2 = {k: randint(1, 3) for k in sample('abcdefgh', randint(3, 6))}
d3 = {k: randint(1, 3) for k in sample('abcdefgh', randint(3, 6))}
print([k for k in d1 if k in d2 and k in d3])

# 方法2：利用集合的交集操作
from functools import reduce

dl = [d1, d2, d3]
print(reduce(lambda a, b: a & b, map(dict.keys, dl)))
