from fastapi.background import P
import numpy as np
# 维度
a = np.array([[1,2],[3,4]])
print(a)
# 最小维度
b = np.array([1,2,3,4,5], ndmin=3)
print(b)
#dtype参数
c = np.array([1,2,3],dtype=np.float32)
print(c)
d = np.dtype('i4')
print(d)
#结构化数据
e = np.dtype([('age',np.int8)])
print(e)
#
dt = np.dtype([('age',np.int8)]) 
f = np.array([(10,),(20,),(30,)], dtype = dt)
print(f)
print(f['age'])

#暂时放弃学习
#有点深奥