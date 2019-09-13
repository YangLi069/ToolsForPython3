#保持字典原有的顺序
#方法1：利用OrderedDict()
from collections import OrderedDict
from random import shuffle

players = list('abcdefgh')
shuffle(players)
od = OrderedDict()
for i,p in enumerate(players, 1):
    od[p]=i

from itertools import islice
def query_by_order(od, a, b=None):
    a-=1
    if b is None:
        b=a+1
    return list(islice(od,a,b))

print(query_by_order(od,1,3))