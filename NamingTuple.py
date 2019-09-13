#如何为元组中的每个元素命名，提高可读性
#方法1：利用枚举类型
student = ('Jim', 16, 'male', 'Jim@gmail.com')
from enum import IntEnum
class StudentEnum(IntEnum):
    NAME = 0
    AGE = 1
    SEX = 2
    EMAIL = 3
print(student[StudentEnum.AGE])
print(student[StudentEnum.SEX])

# 方法2：利用namedtuple创建命名元组
from collections import namedtuple
Student = namedtuple('Student', ['name','age','sex','email'])
s2 = Student('Jim', 16, 'male', 'Jim@gmail.com')
print(s2.age)
print(s2.name)