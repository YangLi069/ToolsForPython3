#根据字典中值的大小排序
#方法1：将字典中的项转化为（值，键）元组。（列表解析或zip）
from random import randint
d = {k:randint(60,100) for k in 'abcdefgh'}
l = [(v, k) for k, v in d.items()]
print(sorted(l, reverse=True))
#list(zip(d.values(), d.keys()))

#方法2：传递sorted函数的key参数
p = sorted(d.items(), key=lambda item:item[1], reverse=True)
list(enumerate(p, 1)) #1表示起始值
for i, (k,v) in enumerate(p,1):
    d[k] = (i,v)
    