def logger(func):
    def wrapper(*args, **kwargs):
        if not hasattr(func, 'is_recursive'):
            print(f"开始执行函数 {func.__name__}")
            print(f"输入参数: args={args}, kwargs={kwargs}")

        result = func(*args, **kwargs)

        if not hasattr(func, 'is_recursive'):
            print(f"函数 {func.__name__} 返回值: {result}")

        return result

    return wrapper

@logger
def factorial(n):
    if n == 0:
        return 1
    else:
        factorial.is_recursive = True
        result = n * factorial(n - 1)
        del factorial.is_recursive
        return result

if __name__ == "__main__":
    factorial(5)

