def get_yield():
    for i in range(1,6):
        print(f"准备返回{i}")
        yield i
        print(f"已经返回{i}")

gen = get_yield()
print(next(gen))
print(next(gen))
next(gen)
print(next(gen))