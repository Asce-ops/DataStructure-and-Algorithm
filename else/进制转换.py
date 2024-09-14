import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent)) # Path(__file__) 获取的当前 py 文件的路径
from Stack import ArrayStack
from HashMap import HashMapOpenAddressing as HashMap

# 只讨论正数的进制转换

def From10BaseConverter(num: int, to_base: int) -> str:
    '''十进制转其他进制'''
    digits: str = '0123456789ABCDEF'
    stack: ArrayStack = ArrayStack()
    while num > 0:
        stack.push(item=num % to_base)
        num //= to_base
    result: str = str()
    while len(stack) > 0:
        result += digits[stack.pop()]
    return result



def To10BaseConverter(num: str, from_base: int) -> int:
    '''其他进制转十进制'''
    digits: HashMap = HashMap()
    for i in '0123456789':
        digits[ord(i)] = ord(i) - 48 # ord('0') == 48
    for i in 'ABCDEF':
        digits[ord(i)] = ord(i) - 55 # ord('A') == 65
    result: int = 0
    exp: int = len(num) - 1
    for i in num:
        result += digits[ord(i)] * (from_base**exp)
        exp -= 1
    return result



def BaseConverter(num: str, from_base: int, to_base: int) -> str:
    '''任意进制间转换'''
    if from_base == 10:
        return From10BaseConverter(num=int(num), to_base=to_base)
    return From10BaseConverter(num=To10BaseConverter(num=num, from_base=from_base), to_base=to_base)



if __name__ == '__main__':
    a: str = From10BaseConverter(num=233, to_base=2)
    print(a)
    b: int = To10BaseConverter(num=a, from_base=2)
    print(b)
    print(BaseConverter(num='351', from_base=8, to_base=16))
    print(BaseConverter(num='E9', from_base=16, to_base=8))