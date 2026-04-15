from collections import namedtuple
from dataclasses import dataclass, field
import re
from typing import Union
from typing import List
from typing import Dict
from typing import Tuple
from pydantic import BaseModel, EmailStr, Field
from pydantic.type_adapter import P

print("python is a good language")

# type hints
x: int = 10
y: str =  "hello python"
z: Union[int, float] = 3.5

print(x)
print(y)
print(z)

# 元组列表字典
list: List[int] = [1, 2, 3, 4, 5]
tuple: Tuple[int, str, float] = (1, "hello", 3.5)
dict: Dict[str, int] = {"apple": 1, "banana": 2, "cherry": 3}
print(list)
print(tuple)
print(dict)

#函数

def add(a:int , b:int) -> str:
    print(type(str(a) + str(b)))
    return str(a) + str(b)
print(add(1, 2))


#类
play = namedtuple('play', ['name', 'age', 'gender'])
jack = play('jack', 20, 'male')

print(jack.name)
print(jack.age)
print(jack.gender)

# 自定义类
class Person:
    def __init__(self, name:str, age:int, gender:str):
        self.name = name
        self.age = age
        self.gender = gender
    def __gt__(self, other):
        return self.age > other.age
    def __eq__(self, other):
        return self.age == other.age
    def __repr__(self) -> str:
        return f'Person({self.name}, {self.age}, {self.gender})'

tom = Person('tom', 20, 'male')
marry = Person('marry', 18, 'female')

# tom > marry
print(tom > marry)
print(tom == marry)
print(tom)

# dataclass
@dataclass
class AI:
    name: str
    age: int
    gender: str

ai1 = AI('jack', 20, 'male')
@dataclass
class AITeam:
    name:str     
    members: List[AI] = field(default_factory= lambda:[ai1])
AI_Team = AITeam('AI_Team')
print(AI_Team)

ai2 = AI('marry', 18, 'female')
AI_Team = AITeam('AI_Team', [ai1, ai2])

print(AI_Team)

# Pydantic BaseModel
class User(BaseModel):
    name: str = Field(...,min_length=3,max_length=10,description='用户名')
    age: int = Field(...,ge=18 , le=100,description='年龄')
    email: EmailStr = Field(...,description='邮箱')
user_data = {
    'name': 'John',
    'age': 18,
    'email': 'john@example.com'
}
user1 = User(**user_data)
user2 = User(name='Jane', age=25, email='jane@example.com')
print(user1)
print(user2)


# 列表推导：[x for x in list if condition]

nums = [1,2,3,4,5,6,7,8]
evens = []
evens = [num for num in nums if num % 2 == 1]
print(evens)



# 装饰器
def function1(func):
    print("装饰器被调用")
    return func

@function1
def say_hello():
    print("hello")

say_hello()

# 装饰器原理

def timer(func):
    print("第一次执行")
    def wrapper(*args,**kwargs):
        print("计时开始1")
        func(*args,**kwargs)
        print("进入func")
    return wrapper
#
print("计时开始")
#

@timer
def main(a):
    a = 3
    print(f"{a}执行中")

#
main(1)    
print("执行结束")