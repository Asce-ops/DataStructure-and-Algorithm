from typing import Final, Generic, TypeVar, Optional, List, Tuple, Hashable , override

from utils import Iterator



K = TypeVar(name="K", bound=Hashable) # 声明一个类型参数，不宜对其进行 type hints
V = TypeVar(
            name="V", 
            # covariant=True
        )

class Pair(Generic[K, V]):
    """键值对"""
    def __init__(self, key: K, val: V) -> None:
        """构造方法

        Args:
            key (K): 键
            val (V): 值
        """
        self._key: K = key # 键
        self._val: V = val # 值

class HashMapOpenAddressing(Generic[K, V]):
    """
    基于数组实现的开放寻址哈希表；
    采用惰性删除机制，否则再哈希过程中可能会提前停止；
    除了更新键值对，其他操作时不要改变键值对的存放位置
    """
    _TOMBSTONE: Final[Pair] = Pair(key=-1, val=None) # 删除标记（不可变）
    capacity: Final[int] = 10 # 初始容量（不可变）
    extend_ratio: Final[int] = 2 # 扩容系数（不可变）
    load_threshold: Final[float] = 0.75 # 触发扩容的负载因子阈值（不可变）

    def __init__(self) -> None:
        """构造方法"""
        self._capacity: int = HashMapOpenAddressing.capacity # 哈希表容量
        self._bucket: List[Optional[Pair[K, V]]] = [None] * self._capacity # 数组桶
        self._size: int = 0 # 键值对数量

    @staticmethod # 静态方法
    def Hash(key: K) -> int:
        """哈希算法

        Args:
            key (K): 键

        Returns:
            int: 键的哈希值
        """
        return hash(key)

    def hash_func(self, key: K) -> int:
        """哈希函数

        Args:
            key (K): 键

        Returns:
            int: 键的哈希函数值
        """
        return HashMapOpenAddressing.Hash(key=key) % self._capacity
    
    def rehash(self, old_hash: int) -> int:
        """通过再哈希来开放寻址

        Args:
            old_hash (int): 旧哈希函数值

        Returns:
            int: 新哈希函数值
        """
        k: int = 1 # 再探测时如果不能遍历所有的桶又无法触发扩容机制，则可能陷入死循环（探测到的永远是被占据的桶）
        return (old_hash + k) % self._capacity # 线性探测
    
    def load_factor(self) -> float:
        """查看负载因子

        Returns:
            float: 负载因子
        """
        return self._size / self._capacity
    
    def put(self, key: K, val: V) -> None:
        """新增或更新键值对

        Args:
            key (K): 键
            val (V): 值
        """
        if self.load_factor() >= HashMapOpenAddressing.load_threshold: # 扩容
            self._extend()
        idx: int = self.hash_func(key=key)
        first_blank: Optional[int] = None # 记录遇到的首个空桶（存储了 None 或删除标记）
        while self._bucket[idx] is not None: # 扩容机制保证了数组中一定有 None 的存在
            if self._bucket[idx]._key == key: # type: ignore # 键存在则更新其对应值
                if first_blank is not None: # 将元素移至距离探测起点更近的空桶，减少查找时所需的哈希次数
                    self._bucket[idx] = HashMapOpenAddressing._TOMBSTONE
                    self._bucket[first_blank] = Pair(key=key, val=val)
                else:
                    self._bucket[idx]._val = val # type: ignore
                return
            if first_blank is None: # 最多只会触发一次
                if (self._bucket[idx] is HashMapOpenAddressing._TOMBSTONE) or (self._bucket[idx] is None):
                    first_blank = idx
            idx = self.rehash(old_hash=idx)
        # 探测到 None 表示键不存在，如果键存在则其应该被存储在此处（探测到删除标记不能证明键不存在）
        if first_blank is not None:
            idx = first_blank
        self._bucket[idx] = Pair(key=key, val=val)
        self._size += 1

    def index(self, key: K) -> int:
        """确定索引位置

        Args:
            key (K): 键

        Raises:
            KeyError: 键在哈希表中不存在

        Returns:
            int: 哈希表中存放键的位置
        """
        idx: int = self.hash_func(key=key)
        while self._bucket[idx] is not None: # 扩容机制保证了数组中一定有 None 的存在
            if self._bucket[idx]._key == key: # type: ignore # 键存在
                return idx
            idx = self.rehash(old_hash=idx)
        raise KeyError(f"{key}不在哈希表中")

    def remove(self, key: K) -> None:
        """删除键值对

        Args:
            key (K): 待删除的键
        """
        idx: int = self.index(key=key)
        self._bucket[idx] = HashMapOpenAddressing._TOMBSTONE
        self._size -= 1
    
    def get(self, key: K) -> V:
        """查询键值对

        Args:
            key (K): 待查询的键

        Returns:
            V: 值
        """
        idx: int = self.index(key=key)
        return self._bucket[idx]._val # type: ignore

    def _extend(self) -> None:
        """扩容"""
        cur: List[Optional[Pair]] = self._bucket
        prev_capacity: int = self._capacity
        self._capacity *= HashMapOpenAddressing.extend_ratio
        self._bucket = [None] * self._capacity
        i: int = 0 # 当前桶
        n: int = 0 # 已经复制了的元素个数
        while i < prev_capacity:
            if n == self._size:
                break
            item: Optional[Pair[K, V]] = cur[i]
            i += 1
            if (item is not None) and (item is not HashMapOpenAddressing._TOMBSTONE):
                idx: int = self.hash_func(key=item._key)
                while self._bucket[idx] is not None:
                    idx = self.rehash(old_hash=idx)
                self._bucket[idx] = item
                n += 1

    def keys(self) -> List[K]:
        """查看所有键

        Returns:
            List[K]: 将哈希表中的键以列表的形式返回
        """
        result: List[Optional[K]] = [None] * self._size
        idx: int = 0
        for i in range(self._capacity):
            item: Optional[Pair[K, V]] = self._bucket[i]
            if (item is not None) and (item is not HashMapOpenAddressing._TOMBSTONE):
                result[idx] = item._key
                idx += 1
            if idx >= self._size:
                break
        return result # type: ignore
    
    def values(self) -> List[V]:
        """查看所有值

        Returns:
            List[K]: 将哈希表中的值以列表的形式返回
        """
        result: List[Optional[V]] = [None] * self._size
        idx: int = 0
        for i in range(self._capacity):
            item: Optional[Pair[K, V]] = self._bucket[i]
            if (item is not None) and (item is not HashMapOpenAddressing._TOMBSTONE):
                result[idx] = item._val
                idx += 1
            if idx >= self._size:
                break
        return result # type: ignore
    
    def items(self) -> List[Tuple[K, V]]:
        """查看所有键值对

        Returns:
            List[K]: 将哈希表中的键值对元组以列表的形式返回
        """
        result: List[Optional[Tuple[K, V]]] = [None] * self._size
        idx: int = 0
        for i in range(self._capacity):
            item: Optional[Pair[K, V]] = self._bucket[i]
            if (item is not None) and (item is not HashMapOpenAddressing._TOMBSTONE):
                result[idx] = (item._key, item._val)
                idx += 1
            if idx >= self._size:
                break
        return result # type: ignore
    
    def __getitem__(self, key: K) -> V:
        """查询键值对

        Args:
            key (K): 待查询的键

        Returns:
            V: 值
        """
        return self.get(key=key)
    
    def __setitem__(self, key: K, val: V) -> None:
        """新增或更新键值对

        Args:
            key (K): 键
            val (V): 值
        """
        self.put(key=key, val=val)

    def __delitem__(self, key: K) -> None:
        """删除键值对

        Args:
            key (K): 待删除的键
        """
        self.remove(key=key)

    def __len__(self) -> int:
        """查看哈希表长度

        Returns:
            int: 哈希表中键值对数量
        """
        return self._size
    
    def __contains__(self, key: K) -> bool:
        """哈希表中是否存在指定键

        Args:
            val (K): 键

        Returns:
            bool: 键在哈希表中是否存在
        """
        try:
            self.index(key=key)
            return True
        except KeyError:
            return False
    
    class Itr(Iterator):
        """该类配套的迭代器"""
        def __init__(self, outer: "HashMapOpenAddressing[K, V]") -> None:
            """构造方法

            Args:
                outer (HashMapOpenAddressing[K, V]): 指向外部类的引用
            """
            self.outer: HashMapOpenAddressing[K, V] = outer # type: ignore
            self.cursor: int = 0 # 当前桶
            self.had: int = 0 # 已经遍历了的元素的个数

        @override
        def __next__(self) -> K:
            """实现 Iterator 接口声明的 __next__ 方法

            Raises:
                StopIteration: 停止迭代

            Returns:
                K: 
            """
            item: Optional[Pair[K, V]] # type: ignore
            while self.cursor < self.outer._capacity:
                if self.had == self.outer._size:
                    break
                item = self.outer._bucket[self.cursor] # type: ignore
                self.cursor += 1
                if (item is not None) and (item is not HashMapOpenAddressing._TOMBSTONE):
                    self.had += 1
                    return item._key
            raise StopIteration

    def __iter__(self) -> Itr:
        """使自身可迭代

        Returns:
            Itr: 类内部实现的迭代器
        """
        return self.Itr(outer=self)



class Node(Generic[K, V]):
    """链表节点"""
    def __init__(self, key: K, val: V) -> None:
        """构造方法

        Args:
            key (K): 键
            val (V): 值
        """
        self._key: K = key
        self._val: V = val
        self.next: Optional[Node[K, V]] = None

class HashMapChaining(Generic[K, V]):
    """链式地址哈希表，数组的每一个桶存储的都是节点"""
    capacity: Final[int] = 13 # 初始容量（不可变）
    extend_ratio: Final[int] = 2 # 扩容系数（不可变）
    avg_threshold: Final[int] = 8 # 平均每个桶可以存储的最大元素个数（用于触发扩容，不可变）

    def __init__(self) -> None:
        """构造方法"""
        self._capacity: int = HashMapChaining.capacity
        self._bucket: List[Optional[Node[K, V]]] = [None] * self._capacity
        self._size: int = 0
        

    @staticmethod # 静态方法（用类名或者实例来调用）
    def Hash(key: K) -> int:
        """哈希算法

        Args:
            key (K): 键

        Returns:
            int: 键的哈希值
        """
        return hash(key)

    def hash_func(self, key: K) -> int:
        """哈希函数

        Args:
            key (K): 键

        Returns:
            int: 键的哈希函数值
        """
        return HashMapChaining.Hash(key=key) % self._capacity

    def put(self, key: K, val: V) -> None:
        """新增或更新键值对

        Args:
            key (K): 键
            val (V): 值
        """
        if self._size >= HashMapChaining.avg_threshold * self._capacity: # 扩容
            self._extend()
        idx: int = self.hash_func(key=key)
        if self._bucket[idx] is not None:
            cur: Node[K, V] = self._bucket[idx] # type: ignore
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
    
    def remove(self, key: K) -> None:
        """删除键值对

        Args:
            key (K): 待删除的键
        """
        idx: int = self.hash_func(key=key)
        if self._bucket[idx] is not None:
            cur: Node[K, V] = self._bucket[idx] # type: ignore
            if cur._key == key:
                self._bucket[idx] = cur.next
                cur.next = None # 便于内存回收
                self._size -= 1
                return
            while cur.next is not None: # 在 cur 定位到某个桶时，这个桶在这之前已经被检查过了
                if cur.next._key == key:
                    tmp: Node = cur.next
                    cur.next = tmp.next
                    tmp.next = None # 便于内存回收
                    self._size -= 1
                    return
                cur = cur.next
        raise KeyError(f"{key}不在哈希表中")
    
    def get(self, key: K) -> V:
        """查询键值对

        Args:
            key (K): 待查询的键

        Returns:
            V: 值
        """
        idx: int = self.hash_func(key=key)
        cur: Optional[Node[K, V]] = self._bucket[idx]
        while cur is not None:
            if cur._key == key: # 键存在，返回值
                return cur._val
            cur = cur.next
        raise KeyError(f"{key}不在哈希表中")
    
    def _extend(self) -> None:
        """扩容"""
        cur: List[Optional[Node[K, V]]] = self._bucket
        prev_capacity: int = self._capacity
        self._capacity *= HashMapChaining.extend_ratio
        self._bucket = [None] * self._capacity
        i: int = 0 # 当前桶
        n: int = 0 # 已经复制了的元素个数
        item: Optional[Node[K, V]] = cur[i] # 当前节点
        while i < prev_capacity:
            if n == self._size:
                break
            if item is not None:
                idx: int = self.hash_func(key=item._key)
                tmp: Optional[Node[K, V]] = self._bucket[idx]
                self._bucket[idx] = item # 在链表头部新增节点
                item = item.next
                self._bucket[idx].next = tmp # type: ignore # 更新完 item 再更新链表头节点的下一个指向
                n += 1
            else:
                i += 1
                item = cur[i]
    
    def keys(self) -> List[K]:
        """查看所有键

        Returns:
            List[K]: 将哈希表中的键以列表的形式返回
        """
        result: List[Optional[K]] = [None] * self._size
        idx: int = 0
        for i in range(self._capacity):
            cur: Optional[Node[K, V]] = self._bucket[i]
            while cur is not None:
                result[idx] = cur._key
                idx += 1
                cur = cur.next
        return result # type: ignore
    
    def values(self) -> List[V]:
        """查看所有值

        Returns:
            List[K]: 将哈希表中的值以列表的形式返回
        """
        result: List[Optional[V]] = [None] * self._size
        idx: int = 0
        for i in range(self._capacity):
            cur: Optional[Node[K, V]] = self._bucket[i]
            while cur is not None:
                result[idx] = cur._val
                idx += 1
                cur = cur.next
        return result # type: ignore
    
    def items(self) -> List[Tuple[K, V]]:
        """查看所有键值对

        Returns:
            List[K]: 将哈希表中的键值对元组以列表的形式返回
        """
        result: List[Optional[Tuple[K, V]]] = [None] * self._size
        idx: int = 0
        for i in range(self._capacity):
            cur: Optional[Node[K, V]] = self._bucket[i]
            while cur is not None:
                result[idx] = (cur._key, cur._val)
                idx += 1
                cur = cur.next
        return result # type: ignore

    def __getitem__(self, key: K) -> V:
        """查询键值对

        Args:
            key (K): 待查询的键

        Returns:
            V: 值
        """
        return self.get(key=key)
    
    def __setitem__(self, key: K, val: V) -> None:
        """新增或更新键值对

        Args:
            key (K): 键
            val (V): 值
        """
        self.put(key=key, val=val)

    def __delitem__(self, key: K) -> None:
        """删除键值对

        Args:
            key (K): 待删除的键
        """
        self.remove(key=key)

    def __len__(self) -> int:
        """查看哈希表长度

        Returns:
            int: 哈希表中键值对数量
        """
        return self._size
    
    def __contains__(self, key: K) -> bool:
        """哈希表中是否存在指定键

        Args:
            val (K): 键

        Returns:
            bool: 键在哈希表中是否存在
        """
        try:
            self.get(key=key)
            return True
        except KeyError:
            return False
        
    class Itr(Iterator):
        """该类配套的迭代器"""
        def __init__(self, outer: "HashMapChaining[K, V]") -> None:
            """构造方法

            Args:
                outer (HashMapChaining[K, V]): 指向外部类的引用
            """
            self.outer: HashMapChaining[K, V] = outer # type: ignore
            self.idx: int = 0 # 当前桶
            self.had: int = 0 # 已经遍历了的元素个数
            self.cursor: Optional[Node] = self.outer._bucket[self.idx] # 当前节点

        @override
        def __next__(self) -> K:
            """实现 Iterator 接口声明的 __next__ 方法

            Raises:
                StopIteration: 停止迭代

            Returns:
                K: 
            """
            result: K # type: ignore
            while self.idx < self.outer._capacity:
                if self.had == self.outer._size:
                    break
                if self.cursor is not None:
                    result = self.cursor._key
                    self.cursor = self.cursor.next
                    self.had += 1
                    return result
                else:
                    self.idx += 1
                    self.cursor = self.outer._bucket[self.idx]
            raise StopIteration

    def __iter__(self) -> Itr:
        """使自身可迭代

        Returns:
            Itr: 类内部实现的迭代器
        """
        return self.Itr(outer=self)



if __name__ == "__main__":
    h1: HashMapOpenAddressing[int, str] = HashMapOpenAddressing[int, str](); h2: HashMapChaining[int, str] = HashMapChaining[int, str]()
    for i in range(30):
        h1.put(key=i, val=str(object=i))
        h2.put(key=i, val=str(object=i))
    del h1[3]
    # del h1[3]
    print("开始遍历h1")
    for i in h1:
        print(i)
    print("开始遍历h2")
    for i in h2:
        print(i)
