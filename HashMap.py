# type: ignore

class Pair:
    '''键值对'''
    def __init__(self, key: int, val: str) -> None:
        '''构造方法'''
        self._key: int = key # 键
        self._val: str = val # 值

class HashMapOpenAddressing:
    '''
    基于数组实现的开放寻址哈希表；
    采用惰性删除机制，否则再哈希过程中可能会提前停止；
    除了更新键值对，其他操作时不要改变键值对的存放位置
    '''
    def __init__(self, capacity: int = 13) -> None:
        '''构造方法'''
        self._capacity: int = capacity # 哈希表容量
        self._bucket: list[Pair | None] = [None] * self._capacity # 数组桶
        self._size: int = 0 # 键值对数量
        self._extend_ratio: int = 2 # 扩容系数
        self._load_thres: float = 0.75 # 触发扩容的负载因子阈值
        self._TOMBSTONE: Pair = Pair(key=-1, val='-1') # 删除标记

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
    
    def put(self, key: int, val: str) -> None:
        '''新增或更新键值对'''
        if self.load_factor() >= self._load_thres: # 扩容
            self._extend()
        idx = self.hash_func(key=key)
        first_blank: int | None = None # 记录遇到的首个空栈（存储了 None 或删除标记）
        while self._bucket[idx] is not None: # 扩容机制保证了数组中一定有 None 的存在
            if self._bucket[idx]._key == key: # 键存在则更新其对应值
                if first_blank is not None: # 将元素移至距离探测起点更近的空桶，减少查找时所需的哈希次数
                    self._bucket[idx] = self._TOMBSTONE
                    self._bucket[first_blank] = Pair(key=key, val=val)
                else:
                    self._bucket[idx]._val = val
                return
            if first_blank is None: # 最多只会触发一次
                if (self._bucket[idx] is self._TOMBSTONE) or (self._bucket[idx] is None):
                    first_blank = idx
            idx = self.rehash(old_hash=idx)
        # 探测到 None 表示键不存在，如果键存在则其应该被存储在此处（探测到删除标记不能证明键不存在）
        if first_blank is not None:
            idx = first_blank
        self._bucket[idx] = Pair(key=key, val=val)
        self._size += 1

    def index(self, key: int) -> int:
        '''确定索引位置'''
        idx = self.hash_func(key=key)
        while self._bucket[idx] is not None: # 扩容机制保证了数组中一定有 None 的存在
            if self._bucket[idx]._key == key: # 键存在
                return idx
            idx = self.rehash(old_hash=idx)
        raise KeyError(f'{key}不在哈希表中')

    def remove(self, key: int) -> None:
        '''删除键值对'''
        idx = self.index(key=key)
        self._bucket[idx] = self._TOMBSTONE
        self._size -= 1
    
    def get(self, key: int) -> str:
        '''查询键值对'''
        idx = self.index(key=key)
        return self._bucket[idx]._val

    def _extend(self) -> None:
        '''扩容'''
        cur = self._bucket
        prev_capacity = self._capacity
        self._capacity *= self._extend_ratio
        self._bucket = [None] * self._capacity
        i: int = 0 # 当前桶
        n: int = 0 # 已经复制了的元素个数
        while i < prev_capacity:
            if n == self._size:
                break
            item = cur[i]
            i += 1
            if (item is not None) and (item is not self._TOMBSTONE):
                idx = self.hash_func(key=item._key)
                while self._bucket[idx] is not None:
                    idx = self.rehash(old_hash=idx)
                self._bucket[idx] = item
                n += 1

    def keys(self) -> list[int]:
        '''查看所有键'''
        result = [None] * self._size
        idx = 0
        for i in range(self._capacity):
            item = self._bucket[i]
            if (item is not None) and (item is not self._TOMBSTONE):
                result[idx] = item._key
                idx += 1
            if idx >= self._size:
                break
        return result
    
    def values(self) -> list[str]:
        '''查看所有键'''
        result = [None] * self._size
        idx = 0
        for i in range(self._capacity):
            item = self._bucket[i]
            if (item is not None) and (item is not self._TOMBSTONE):
                result[idx] = item._val
                idx += 1
            if idx >= self._size:
                break
        return result
    
    def __getitem__(self, key: int) -> str:
        return self.get(key=key)
    
    def __setitem__(self, key: int, val: str) -> None:
        self.put(key=key, val=val)

    def __delitem__(self, key: int) -> None:
        self.remove(key=key)

    def __len__(self) -> int:
        return self._size
    
    def __contains__(self, key: int) -> bool:
        try:
            self.index(key=key)
            return True
        except KeyError:
            return False
        
    def __iter__(self):
        self.__idx: int = 0 # 当前桶
        self.__cur: int = 0 # 已经遍历了的元素个数
        return self
    
    def __next__(self) -> int: # 遍历返回键
        while self.__idx < self._capacity:
            if self.__cur == self._size:
                break
            item = self._bucket[self.__idx]
            self.__idx += 1
            if (item is not None) and (item is not self._TOMBSTONE):
                self.__cur += 1
                return item._key
        raise StopIteration


class Node:
    '''链表节点'''
    def __init__(self, key: int, val: str) -> None:
        '''构造方法'''
        self._key: int = key
        self._val: int = val
        self.next: Node | None = None

class HashMapChaining:
    '''链式地址哈希表，数组的每一个桶存储的都是节点'''
    def __init__(self, capacity: int = 13) -> None:
        '''构造方法'''
        self._capacity: int = capacity
        self._bucket: list[Node | None] = [None] * self._capacity
        self._size: int = 0
        self._extend_ratio: int = 2 # 扩容系数
        self._avg_thres: int = 8 # 平均每个桶可以存储的最大元素个数（用于触发扩容）

    @staticmethod # 静态方法（用类名或者实例来调用）
    def hash(key: int) -> int:
        '''哈希算法'''
        return key

    def hash_func(self, key: int) -> int:
        '''哈希函数'''
        return self.hash(key=key) % self._capacity

    def put(self, key: int, val: str) -> None:
        '''新增或更新键值对'''
        if self._size >= self._avg_thres * self._capacity: # 扩容
            self._extend()
        idx = self.hash_func(key=key)
        if self._bucket[idx] is not None:
            cur = self._bucket[idx]
            while cur.next is not None:
                if cur._key == key: # 键存在，更新键值对
                    cur._val = val
                    return
                cur = cur.next
            if cur._key == key: # 检查当前存在的最后一个节点
                cur._val = val
                return
            cur.next = Node(key=key, val=val) # 键不存在，在尾部新增节点
        else: # 桶为空，直接在此处存储元素
            self._bucket[idx] = Node(key=key, val=val)
        self._size += 1
    
    def remove(self, key: int) -> None:
        '''删除键值对'''
        idx = self.hash_func(key=key)
        if self._bucket[idx] is not None:
            cur = self._bucket[idx]
            if cur._key == key:
                self._bucket[idx] = cur.next
                cur.next = None # 便于内存回收
                self._size -= 1
                return
            while cur.next is not None: # 在 cur 定位到某个桶时，这个桶在这之前已经被检查过了
                if cur.next._key == key:
                    tmp = cur.next
                    cur.next = tmp.next
                    tmp.next = None # 便于内存回收
                    self._size -= 1
                    return
                cur = cur.next
        raise KeyError(f'{key}不在哈希表中')
    
    def get(self, key: int) -> str:
        '''查询键值对'''
        idx = self.hash_func(key=key)
        cur = self._bucket[idx]
        while cur is not None:
            if cur._key == key: # 键存在，返回值
                return cur._val
            cur = cur.next
        raise KeyError(f'{key}不在哈希表中')
    
    def _extend(self) -> None:
        '''扩容'''
        cur = self._bucket
        prev_capacity = self._capacity
        self._capacity *= self._extend_ratio
        self._bucket = [None] * self._capacity
        i: int = 0 # 当前桶
        n: int = 0 # 已经复制了的元素个数
        item: Node | None = cur[i] # 当前节点
        while i < prev_capacity:
            if n == self._size:
                break
            if item is not None:
                idx = self.hash_func(key=item._key)
                tmp: Node | None = self._bucket[idx]
                self._bucket[idx] = item # 在链表头部新增节点
                item = item.next
                self._bucket[idx].next = tmp # 更新完 item 再更新链表头节点的下一个指向
                n += 1
            else:
                i += 1
                item = cur[i]
    
    def keys(self) -> list[int]:
        '''查看所有键'''
        result: list[int | None] = [None] * self._size
        idx = 0
        for i in range(self._capacity):
            cur = self._bucket[i]
            while cur is not None:
                result[idx] = cur._key
                idx += 1
                cur = cur.next
        return result
    
    def values(self) -> list[str]:
        '''查看所有值'''
        result: list[str | None] = [None] * self._size
        idx = 0
        for i in range(self._capacity):
            cur = self._bucket[i]
            while cur is not None:
                result[idx] = cur._val
                idx += 1
                cur = cur.next
        return result
    
    def __getitem__(self, key: int) -> str:
        return self.get(key=key)
    
    def __setitem__(self, key: int, val: str) -> None:
        self.put(key=key, val=val)

    def __delitem__(self, key: int) -> None:
        self.remove(key=key)

    def __len__(self) -> int:
        return self._size
    
    def __contains__(self, key: int) -> bool:
        try:
            self.get(key=key)
            return True
        except KeyError:
            return False
        
    def __iter__(self):
        self.__idx: int = 0 # 当前桶
        self.__cur: int = 0 # 已经遍历了的元素个数
        self.__tmp: Node | None = self._bucket[self.__idx] # 当前节点
        return self
    
    def __next__(self) -> int: # 遍历返回键
        while self.__idx < self._capacity:
            if self.__cur == self._size:
                break
            if self.__tmp is not None:
                result = self.__tmp._key
                self.__tmp = self.__tmp.next
                self.__cur += 1
                return result
            else:
                self.__idx += 1
                self.__tmp = self._bucket[self.__idx]
        raise StopIteration
    



if __name__ == '__main__':
    h1, h2 = HashMapOpenAddressing(), HashMapChaining()
    for i in range(30):
        h1.put(key=i, val=str(i))
        h2.put(key=i, val=str(i))
    del h1[3]
    print('开始遍历h1')
    for i in h1:
        print(i)
    print('开始遍历h2')
    for i in h2:
        print(i)
