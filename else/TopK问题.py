import sys
from pathlib import Path

sys.path.append(str(object=Path(__file__).parent.parent)) # Path(__file__) 获取的当前 py 文件的路径

from Heap import MaxHeap, MinHeap



def TopK(data: list[int], k: int, minimum: bool = True):
    '''返回数组最小（大）的前 k 个元素'''
    tmp: list[None] = [None] * k
    for i in range(k):
        tmp[i] = data[i]
    if minimum:
        heap = MaxHeap(data=tmp) # 为了迅速找到当前最小的 k 个元素中的最大值
        for i in range(k, len(data)):
            if data[i] < heap.peek():
                heap.pop() # 先出堆再入堆，否则可能触发扩容
                heap.push(data[i])
    else:
        heap = MinHeap(data=tmp) # 为了迅速找到当前最大的 k 个元素中的最小值
        for i in range(k, len(data)):
            if data[i] > heap.peek():
                heap.pop()
                heap.push(data[i])
    return heap._heap



if __name__ == '__main__':
    data = [9, 8, 6, 6, 7, 5, 2, 1, 4, 3, 6, 2]
    result = TopK(data=data, k=5)
    print(result)
    result2 = TopK(data=data, k=5, minimum=False)
    print(result2)