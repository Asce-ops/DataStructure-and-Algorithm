import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent)) # Path(__file__) 获取的当前 py 文件的路径

from Stack import ArrayStack

def Hanota(n: int, from_pole: ArrayStack, with_pole: ArrayStack, to_pole: ArrayStack) -> None:
    '''n 阶汉诺塔问题：将 n 个盘子按规则从起点柱移动到终点柱'''
    if n == 1: # 递归的基本情况：如果只有一个盘子，直接将其从起点柱移动到终点柱
        to_pole.push(item=from_pole.pop())
        print(f'起点柱：{from_pole.to_list()}，中间柱：{with_pole.to_list()}，终点柱：{to_pole.to_list()}')
    else:
        Hanota(n=n-1, from_pole=from_pole, with_pole=to_pole, to_pole=with_pole) # 将上面 n-1 个盘子从起点柱柱移动到中间柱
        to_pole.push(item=from_pole.pop()) # 将第 n 个盘子从起点柱移动到终点柱
        print(f'起点柱：{from_pole.to_list()}，中间柱：{with_pole.to_list()}，终点柱：{to_pole.to_list()}')
        Hanota(n=n-1, from_pole=with_pole, with_pole=from_pole, to_pole=to_pole) # 将上面 n-1 个盘子从中间柱移动到终点柱



if __name__ == '__main__':
    A: ArrayStack = ArrayStack()
    B: ArrayStack = ArrayStack()
    C: ArrayStack = ArrayStack()

    n: int = 5 # 5阶的汉诺塔问题
    for i in range(n): # 初始化起点柱
        A.push(item=i)

    print(f'3 根柱子的初始状态：\n起点柱：{A.to_list()}， 中间柱：{B.to_list()}，终点柱：{C.to_list()}')
    print('开始移动：')
    Hanota(n=len(A), from_pole=A, with_pole=B, to_pole=C)
    print('结束移动。')