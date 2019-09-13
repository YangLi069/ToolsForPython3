#统计元素出现的次数，找出出现次数最多的元素
#方法1：将序列转换为字典{元素，频度}，根据字典中的值排序
from random import randint
data = [randint(0,20) for _ in range(30)]
d = dict.fromkeys(data,0)
for x in data:
    d[x] += 1

sorted([(v,k) for k, v in d.items()], reverse=True)

import heapq
heapq.nlargest(3, ((v,k) for k, v in d.items()))

#方法2：使用标准库collections中的Counter对象
from collections import Counter
c = Counter(data)
print(c.most_common(3))