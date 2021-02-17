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


# 方法3：使用最小堆
from heapq import heappush, heappop

# 用一个最小堆来保存积分最多的100位用户
# 这样，积分最小的用户刚好在堆顶
top100 = []
users = [100, 100, 100, 20, 23, ...]

# 遍历所有用户
for user in users:
    # 堆未满100，不断压入
    if len(top100) < 100:
        heappush(top100, user)
        continue

    # 如果当前用户积分比堆中积分最少的用户多，则替换
    if user > top100[0]:
        heappop(top100)
        heappush(top100, user)

# 遍历完毕后，现在堆中保存的用户就是积分最多的100位了
