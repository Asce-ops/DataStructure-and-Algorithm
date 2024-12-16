def modexp(x: int, n: int, p: int) -> int:
    """求 x**n % p 的结果"""
    result: int = x % p # x 和 x % p 对模 p 同余
    for _ in range(n - 1):
        result = (result * x) % p
    return result



if __name__ == "__main__":
    print(modexp(x=3, n=1254906, p=10))
    from 进制转换 import BaseConverter
    # print(To10BaseConverter(num="68656C6C6F20776F726C64", from_base=16))
    print(BaseConverter(num="68656C", from_base=16, to_base=10))
    print(BaseConverter(num="6C6F20", from_base=16, to_base=10))
    print(BaseConverter(num="776F72", from_base=16, to_base=10))
    print(BaseConverter(num="6C64", from_base=16, to_base=10))