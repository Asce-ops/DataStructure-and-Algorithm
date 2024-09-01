class MaxHeap:
    '''大顶堆（完全二叉树，任意非叶子节点的值大于等于其子节点的值）'''
    def __init__(self, data: list[int] | None = None) -> None:
        '''构造方法'''
        self._extend_ratio: int = 2 # 每次扩容的倍数
        if data is None: # 初始化一个空堆
            self._capacity: int = 10 # 容量
            self._heap: list[int | None] = [None] * self._capacity
            self._size: int = 0
        else: # 堆化现有数组
            self._capacity: int = len(data)
            self._heap: list[int | None] = [None] * self._capacity
            self._size: int = self._capacity
            last_leaf = (self._size - 2) // 2 # 最后一个非叶子节点（有可能等于-1）
            for i in range(last_leaf + 1, self._size):
                self._heap[i] = data[i]
            for i in range(last_leaf, -1, -1):
                '''
                倒序遍历数组（层序遍历的倒序），依次对每个非叶节点执行“从顶至底堆化”；
                每当堆化一个节点后，以该节点为根节点的子树就形成一个合法的子堆。
                '''
                self._heap[i] = data[i]
                self._sift_down(idx=i)

    def _extend(self) -> None:
        '''扩容'''
        tmp = self._heap
        self._capacity *= self._extend_ratio
        self._heap = [None] * self._capacity
        for i in range(self._size):
            self._heap[i] = tmp[0]

    def push(self, val) -> None:
        '''入堆'''
        if self._size >= self._capacity: # 扩容
            self._extend()
        self._heap[self._size] = val
        self._sift_up(idx=self._size) # 将尾部追加的节点上浮至合适位置
        self._size += 1

    def pop(self) -> int:
        '''出堆'''
        if self._size == 0:
            raise IndexError('堆为空')
        result = self._heap[0]
        self._heap[0] = self._heap[self._size - 1]
        self._heap[self._size - 1] = None
        self._size -= 1 # 因为下沉节点时需要引用堆的长度，务必先更新堆的长度再下沉节点
        self._sift_down(idx=0) # 将交换后新的根节点下沉至合适位置
        return result
    
    def peek(self) -> int:
        '''查看堆顶元素'''
        if self._size == 0:
            raise IndexError('堆为空')
        return self._heap[0]
    
    def _sift_up(self, idx: int) -> None:
        '''上浮节点'''
        while idx > 0: # 根节点无需再上浮
            parent = (idx - 1) // 2 # 父节点的索引
            if self._heap[parent] >= self._heap[idx]: # 无需再修复节点
                break
            self._heap[parent], self._heap[idx] = self._heap[idx], self._heap[parent] # 修复节点
            idx = parent

    def _sift_down(self, idx: int) -> None:
        '''下沉节点'''
        while True:
            left = 2 * idx + 1 # 左子节点的索引
            if left < self._size: # 存在子节点（叶子节点无需再下沉）
                maximum: int = idx # 记录当前节点和其子节点中的最大节点
                if self._heap[left] > self._heap[idx]:
                    maximum = left
                right = 2 * idx + 2 # 右子节点的索引
                if (right < self._size) and (self._heap[right] > self._heap[maximum]):
                    maximum = right
                if maximum != idx: # 需要修复节点
                    self._heap[idx], self._heap[maximum] = self._heap[maximum], self._heap[idx]
                    idx = maximum
                    continue
            break # 无需修复节点

    def __len__(self) -> int:
        return self._size



class MinHeap:
    '''小顶堆（完全二叉树，任意非叶子节点的值小于等于其子节点的值）'''
    def __init__(self, data: list[int] | None = None) -> None:
        '''构造方法'''
        self._extend_ratio: int = 2 # 每次扩容的倍数
        if data is None: # 初始化一个空堆
            self._capacity: int = 10 # 容量
            self._heap: list[int | None] = [None] * self._capacity
            self._size: int = 0
        else: # 堆化
            self._capacity: int = len(data)
            self._heap: list[int | None] = [None] * self._capacity
            self._size: int = self._capacity
            last_leaf = (self._size - 2) // 2 # 最后一个非叶子节点（有可能等于-1）
            for i in range(last_leaf + 1, self._size):
                self._heap[i] = data[i]
            for i in range(last_leaf, -1, -1):
                '''
                倒序遍历堆（层序遍历的倒序），依次对每个非叶节点执行“从顶至底堆化”；
                每当堆化一个节点后，以该节点为根节点的子树就形成一个合法的子堆。
                '''
                self._heap[i] = data[i]
                self._sift_down(idx=i)

    def _extend(self) -> None:
        '''扩容'''
        tmp = self._heap
        self._capacity *= self._extend_ratio
        self._heap = [None] * self._capacity
        for i in range(self._size):
            self._heap[i] = tmp[0]

    def push(self, val) -> None:
        '''入堆'''
        if self._size >= self._capacity: # 扩容
            self._extend()
        self._heap[self._size] = val
        self._sift_up(idx=self._size) # 将尾部追加的节点上浮至合适位置
        self._size += 1

    def pop(self) -> int:
        '''出堆'''
        if self._size == 0:
            raise IndexError('堆为空')
        result = self._heap[0]
        self._heap[0] = self._heap[self._size - 1]
        self._heap[self._size - 1] = None
        self._size -= 1 # 因为下沉节点时需要引用堆的长度，务必先更新堆的长度再下沉节点
        self._sift_down(idx=0) # 将交换后新的根节点下沉至合适位置
        return result
    
    def peek(self) -> int:
        '''查看堆顶元素'''
        if self._size == 0:
            raise IndexError('堆为空')
        return self._heap[0]
    
    def _sift_up(self, idx: int) -> None:
        '''上浮节点'''
        while idx > 0: # 根节点无需再上浮
            parent = (idx - 1) // 2 # 父节点的索引
            if self._heap[parent] <= self._heap[idx]: # 无需再修复节点
                break
            self._heap[parent], self._heap[idx] = self._heap[idx], self._heap[parent] # 修复节点
            idx = parent

    def _sift_down(self, idx: int) -> None:
        '''下沉节点'''
        while True:
            left = 2 * idx + 1 # 左子节点的索引
            if left < self._size: # 存在子节点（叶子节点无需再下沉）
                minimum: int = idx # 记录当前节点和其子节点中的最小节点
                if self._heap[left] < self._heap[idx]:
                    minimum = left
                right = 2 * idx + 2 # 右子节点的索引
                if (right < self._size) and (self._heap[right] < self._heap[minimum]):
                    minimum = right
                if minimum != idx: # 需要修复节点
                    self._heap[idx], self._heap[minimum] = self._heap[minimum], self._heap[idx]
                    idx = minimum
                    continue
            break # 无需修复节点
    
    def __len__(self) -> int:
        return self._size



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
    h: MaxHeap = MaxHeap(data=data)
    print(h._heap)