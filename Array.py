from Iterator import Iterator

class DynamicArray:
    '''使用列表来模拟（动态）数组'''
    def __init__(self, capacity: int = 10) -> None:
        '''构造方法'''
        self._capacity: int = capacity # 数组容量
        self._arr: list[int] = [None] * self._capacity # 实际用于存储元素的数组
        self._size: int = 0 # 当前存储的元素数量
        self._extend_ratio: int = 2 # 每次扩容的倍数

    def append(self, item: int) -> None:
        '''在尾部追加元素'''
        if self._size >= self._capacity: # 容量不足，扩容
            self._extend()
        self._arr[self._size] = item
        self._size += 1 # 更新元素数量

    def insert(self, idx: int, item: int) -> None:
        '''在指定位置插入元素'''
        if idx < 0 or idx > self._size: # 索引越界
            raise IndexError('索引越界')
        if self._size >= self._capacity: # 容量不足，扩容
            self._extend()
        for i in range(self._size, idx, -1): # 从后往前逐个移动元素
            self._arr[i] = self._arr[i-1]
        self._arr[idx] = item
        self._size += 1 # 更新元素数量

    def pop(self, idx: int = -1) -> int:
        '''删除并返回指定位置的元素'''
        if idx not in range(-1 * self._size, self._size): # 索引越界
            raise IndexError('索引越界')
        if idx < 0:
            idx = (idx + self._size) % self._size
        result: int = self._arr[idx]
        for i in range(idx, self._size - 1): # 从前往后逐个移动元素
            self._arr[i] = self._arr[i+1]
        self._arr[self._size-1] = None
        self._size -= 1 # 更新元素数量
        return result

    def remove(self, item: int) -> None:
        '''删除首个指定元素'''
        for i in range(self._size):
            if self._arr[i] == item:
                idx = i # 定位到待删除元素的位置
                # 删除元素
                for i in range(idx, self._size - 1): # 从前往后逐个移动元素
                    self._arr[i] = self._arr[i+1]
                self._arr[self._size-1] = None
                self._size -= 1 # 更新元素数量
                return
        raise ValueError(f'{item}不在数组中')
    
    def _extend(self) -> None:
        '''扩容数组'''
        cur: list[int] = self._arr
        self._capacity *= self._extend_ratio
        self._arr = [None] * self._capacity
        for i in range(self._size): # 将元素逐个复制到新的内存块中
            self._arr[i] = cur[i]

    def get(self, idx: int) -> int:
        '''查看指定位置的元素'''
        if idx not in range(-1 * self._size, self._size): # 索引越界
            raise IndexError('索引越界')
        if idx < 0:
            idx = (idx + self._size) % self._size
        return self._arr[idx]
    
    def set(self, idx: int, item: int) -> None:
        '''修改指定位置的元素'''
        if idx not in range(-1 * self._size, self._size): # 索引越界
            raise IndexError('索引越界')
        if idx < 0:
            idx = (idx + self._size) % self._size
        self._arr[idx] = item

    def index(self, item: int) -> int:
        '''查看首个指定元素的位置'''
        for i in range(self._size):
            if self._arr[i] == item:
                return i
        raise ValueError(f'{item}不在数组中')
    
    def __getitem__(self, idx: int) -> int:
        return self.get(idx=idx)
    
    def __setitem__(self, idx: int, item: int) -> None:
        self.set(idx=idx, item=item)

    def __len__(self) -> int:
        '''获取数组的长度'''
        return self._size
    
    def capacity(self) -> int:
        '''获取数组的当前容量'''
        return self._capacity
    
    def __contains__(self, item: int) -> bool:
        '''数组中是否存在指定元素'''
        for i in range(self._size):
            if self._arr[i] == item:
                return True
        return False
    
    def to_list(self) -> list[int]:
        '''返回列表'''
        result: list[int] = [None] * self._size
        for i in range(self._size):
            result[i] = self._arr[i]
        return result
    
    class Itr(Iterator):
        '''该类配套的迭代器'''
        def __init__(self, outer) -> None:
            self.outer: DynamicArray = outer
            self.cursor: int = 0

        def __next__(self) -> int:
            '''实现 Iterator 接口声明的 __next__ 方法'''
            cur: int = self.cursor
            if cur >= self.outer._size:
                raise StopIteration 
            self.cursor += 1
            return self.outer._arr[cur]

    def __iter__(self) -> Itr:
        '''使自身可迭代'''
        return self.Itr(outer=self)



if __name__ == '__main__':
    arr: DynamicArray = DynamicArray()
    for i in range(10):
        arr.append(i)
    print(arr.to_list())
    for i in arr:
        print(i)