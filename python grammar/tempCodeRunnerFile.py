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