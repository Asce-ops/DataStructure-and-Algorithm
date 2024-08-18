# type: ignore

class Pair:
    '''键值对'''
    def __init__(self, key: int, val: str) -> None:
        '''构造方法'''
        self._key: int = key # 键
        self._val: str = val # 值

class HashMapOpenAddressing:
    '''
    基于数组实现的开放寻址哈希表，
    采用惰性删除机制，否则再哈希过程中可能会提前停止
    '''
    def __init__(self) -> None:
        '''构造方法'''
        self._capacity = 13 # 哈希表容量
        self._bucket: list[Pair | None] = [None] * self._capacity # 数组桶
        self._size: int = 0 # 键值对数量
        self._extend_ratio: int = 2 # 扩容系数
        self._load_thres: float = 0.75 # 触发扩容的负载因子阈值
        self._TOMBSTONE = Pair(key=-1, val='-1') # 删除标记

    @staticmethod # 静态方法（用类名或者实例来调用）
    def hash(key: int) -> int:
        '''哈希算法'''
        return key

    def hash_func(self, key: int) -> int:
        '''哈希函数'''
        return self.hash(key=key) % self._capacity
    
    def rehash(self, old_hash: int) -> int:
        '''通过再哈希来开放寻址'''
        k = 1 # 再探测时如果不能遍历所有的桶又无法触发扩容机制，则可能陷入死循环（探测到的永远是被占据的桶）
        return (old_hash + k) % self._capacity # 线性探测
    
    def load_factor(self) -> float:
        '''负载因子'''
        return self._size / self._capacity
    
    def index(self, key: int) -> int:
        '''确定索引位置'''
        idx = self.hash_func(key=key)
        first_tombstone: int | None = None # 记录遇到的首个删除标记的位置
        while self._bucket[idx] is not None:
            if self._bucket[idx]._key == key:
                if first_tombstone is not None: # 将元素移至距离探测起点更近的空桶，减少探测所需的哈希次数
                    self._bucket[first_tombstone] = self._bucket[idx]
                    self._bucket[idx] = self._TOMBSTONE
                    idx = first_tombstone
                return idx
            if self._bucket[idx] is None: # 该桶从未存储过元素，如果键存在则其应该被存储在此处
                break
            if first_tombstone is None and self._bucket[idx] is self._TOMBSTONE: # 最多只会触发一次
                first_tombstone = idx
            idx = self.rehash(old_hash=idx)
        raise ValueError(f'{key}不在哈希表中')
    
    def put(self, key: int, val: str) -> None:
        '''新增键值对'''
        if self.load_factor() >= self._load_thres: # 扩容
            self._extend()
        idx = self.hash_func(key=key)
        while (self._bucket[idx] is not None) and (self._bucket[idx] is not self._TOMBSTONE): # 找到一个空桶
            if 
            idx = self.rehash(old_hash=idx)
        