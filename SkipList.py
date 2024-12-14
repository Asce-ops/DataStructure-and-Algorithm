from random import randint
from typing import Generic, TypeVar, Optional, List, Tuple, override

from Stack import ArrayStack
from utils import Iterator, Comparable



K = TypeVar(name="K", bound=Comparable)
V = TypeVar(
            name="V", 
            # covariant=True
        )

class HeaderNode:
    """头节点"""
    def __init__(self) -> None:
        """构造方法"""
        self._next: Optional[DataNode] = None # 指向该层的首个数据节点
        self._down: Optional[HeaderNode] = None # 指向下一层的头节点

class DataNode(Generic[K, V]):
    """数据节点"""
    def __init__(self, key: K, val: V) -> None:
        """构造方法

        Args:
            key (K): 键
            val (V): 值
        """
        self._key: K = key
        self._val: V = val
        self._next: Optional[DataNode[K, V]] = None # 指向该层的下一个数据节点
        self._down: Optional[DataNode[K, V]] = None # 指向塔的下一层数据节点
        self._height: int = 0 # 用于记录塔高，只在每一座塔的顶层节点中保持准确

class SkipList(Generic[K, V]):
    """跳表"""
    def __init__(self) -> None:
        """构造方法"""
        self._head: HeaderNode = HeaderNode() # 表头
        self._size: int = 0
    
    def get(self, key: K) -> V:
        """查询键值对

        Args:
            key (K): 待查询的键

        Raises:
            KeyError: 键在跳表表中不存在

        Returns:
            V: 值
        """
        cur: HeaderNode | DataNode[K, V] = self._head
        while cur is not None:
            if cur._next is None: # 没有下一个数据节点则跳到下一层
                cur = cur._down # type: ignore
            else: # cur._next 不可能是头节点，实际上在该分支中只能是数据节点
                if key == cur._next._key: # 查找到的一定是键对应塔的最高层的数据节点
                    return cur._next._val
                elif key < cur._next._key: # 每一层是一个有序链表，此时往右的所有节点只会更大，应该降到下一层
                    cur = cur._down # type: ignore
                else: # key > cur._next._key
                    cur = cur._next       
        raise KeyError(f"{key}在跳表中不存在")
    
    def put(self, key: K, val: V) -> None:
        """新增或更新键值对

        Args:
            key (K): 键
            val (V): 值
        """
        cur: HeaderNode | DataNode = self._head
        stack: ArrayStack[HeaderNode | DataNode] = ArrayStack() # 要去到下一层时将当前节点入栈
        while cur is not None: # 循环结束时 cur 是第 0 层某节点 _down 的指向
            if cur._next is None:
                stack.push(item=cur)
                cur = cur._down # type: ignore
            else: # cur._next 不可能是头节点，实际上在该分支中只能是数据节点
                if key == cur._next._key: # 查找到的一定是键对应塔的最高层的数据节点
                    """键存在，更新对应值"""
                    cur = cur._next
                    while cur is not None:
                        cur._val = val # type: ignore
                        cur = cur._down # type: ignore
                    return
                elif key < cur._next._key: # 每一层是一个有序链表，此时往右的所有节点只会更大，应该降到下一层
                    stack.push(item=cur)
                    cur = cur._down # type: ignore
                else: # key > cur._next._key
                    cur = cur._next
        # 定位到插入位置，新的键值对放在栈顶元素的后面
        lowest_level: HeaderNode | DataNode[K, V] = stack.pop()
        data: DataNode[K, V] = DataNode[K, V](key=key, val=val)
        data._next = lowest_level._next
        lowest_level._next = data
        top: DataNode[K, V] = data # 塔顶
        height: int = 1
        while randint(a=0, b=1) == 1:
            height += 1
            if stack.is_empty(): # 插入节点所在的塔的高度超过了现有层数
                new_head: HeaderNode = HeaderNode()
                data = DataNode(key=key, val=val)
                data._down = top
                new_head._next = data
                new_head._down = self._head
                self._head = new_head
                top = data
            else:
                prev_level: HeaderNode | DataNode[K, V] = stack.pop()
                data = DataNode(key=key, val=val)
                data._down = top
                data._next = prev_level._next
                prev_level._next = data
                top = data
        top._height = height
        self._size += 1
        
    def remove(self, key: K) -> None:
        """删除键值对

        Args:
            key (K): 待删除的键

        Raises:
            KeyError: 待删除的键在跳表中不存在
        """
        cur: HeaderNode | DataNode[K, V] = self._head
        while cur is not None:
            if cur._next is None: # 没有下一个数据节点则跳到下一层
                cur = cur._down # type: ignore
            else:
                if key == cur._next._key: # 定位到了键所在的节点
                    """cur 是键所在节点的前一个节点"""
                    tmp: DataNode = cur._next
                    cur._next = tmp._next
                    """便于内存回收"""
                    tmp._next = None
                    tmp._down = None
                    while cur._down is not None: # 循环结束时已到达第 0 层
                        cur = cur._down
                        while cur._next._key != key: # type: ignore # 循环结束时`cur.next.key == key`
                            cur = cur._next # type: ignore
                        """cur 是键所在节点的前一个节点"""
                        tmp = cur._next # type: ignore
                        cur._next = tmp._next
                        """便于内存回收"""
                        tmp._next = None
                        tmp._down = None
                    self._size -= 1
                    return
                elif key < cur._next._key: # 每一层是一个有序链表，此时往右的所有节点只会更大，应该降到下一层
                    cur = cur._down # type: ignore
                else: # key > cur._next._key
                    cur = cur._next
        raise KeyError(f"{key}在跳表中不存在")

    def __contains__(self, key: K) -> bool:
        """跳表中是否存在指定键

        Args:
            val (K): 键

        Returns:
            bool: 键在跳表中是否存在
        """   
        try:
            self.get(key=key)
            return True
        except KeyError:
            return False
    
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
        """查看跳表中存储的键值对数量

        Returns:
            int: 跳表中键值对数量
        """
        return self._size
    
    def keys(self) -> List[K]:
        """查看所有键

        Returns:
            List[K]: 将跳表中的键以列表的形式返回
        """
        result: List[Optional[K]] = [None] * self._size
        cur: HeaderNode | DataNode[K, V] = self._head
        idx: int = 0
        while cur._down is not None: # 循环结束时定位到第 0 层的头节点
            cur = cur._down
        while cur._next is not None:
            result[idx] = cur._next._key
            cur = cur._next
            idx += 1
        return result # type: ignore
    
    def values(self) -> List[V]:
        """查看所有值

        Returns:
            List[K]: 将跳表中的键以列表的形式返回
        """        
        result: List[Optional[V]] = [None] * self._size
        cur: HeaderNode | DataNode[K, V] = self._head
        idx: int = 0
        while cur._down is not None: # 循环结束时定位到第 0 层的头节点
            cur = cur._down
        while cur._next is not None:
            result[idx] = cur._next._val
            cur = cur._next
            idx += 1
        return result # type: ignore
    
    def items(self) -> List[Tuple[K, V]]:
        """查看所有键值对

        Returns:
            List[K]: 将哈希表中的键值对元组以列表的形式返回
        """
        result: List[Optional[Tuple[K, V]]] = [None] * self._size
        cur: HeaderNode | DataNode = self._head
        idx: int = 0
        while cur._down is not None: # 循环结束时定位到第 0 层的头节点
            cur = cur._down
        while cur._next is not None:
            result[idx] = (cur._next._key, cur._next._val)
            cur = cur._next
            idx += 1
        return result # type: ignore

    def height(self, key: K) -> int:
        """查看指定键对应塔的塔高

        Args:
            key (K): 待查询的键

        Raises:
            KeyError: 键在跳表中不存在

        Returns:
            int: 指定键对应塔的塔高
        """        
        cur: Optional[HeaderNode | DataNode[K, V]] = self._head
        while cur is not None:
            if cur._next is None: # 没有下一个数据节点则跳到下一层
                cur = cur._down
            else: # cur._next 不可能是头节点，实际上在该分支中只能是数据节点
                if key == cur._next._key: # 查找到的一定是键对应塔的最高层的数据节点
                    return cur._next._height
                elif key < cur._next._key: # 每一层是一个有序链表，此时往右的所有节点只会更大，应该降到下一层
                    cur = cur._down
                else: # key > cur._next._key
                    cur = cur._next       
        raise KeyError(f"{key}在跳表中不存在")
    
    class Itr(Iterator):
        """该类配套的迭代器"""
        def __init__(self, outer: "SkipList[K, V]") -> None:
            """构造方法

            Args:
                outer (SkipList[K, V]): 指向外部类的引用
            """
            self.outer: SkipList[K, V] = outer # type: ignore
            self.cursor: Optional[HeaderNode | DataNode[K, V]] = self.outer._head # type: ignore
            while self.cursor._down is not None: # 循环结束时定位到第 0 层的头节点
                self.cursor = self.cursor._down
            self.cursor = self.cursor._next # 定位到第 0 层的首个数据节点
        
        @override
        def __next__(self) -> K:
            """实现 Iterator 接口声明的 __next__ 方法

            Raises:
                StopIteration: 停止迭代

            Returns:
                K: 
            """
            result: K # type: ignore
            while self.cursor is not None:
                result = self.cursor._key # type: ignore
                self.cursor = self.cursor._next
                return result
            raise StopIteration
        
    def __iter__(self) -> Itr:
        """使自身可迭代

        Returns:
            Itr: 类内部实现的迭代器
        """
        return self.Itr(outer=self)



if __name__ == "__main__":
    s: SkipList[int, str] = SkipList[int, str]()
    for i in range(10):
        s.put(key=i, val=str(object=i))
    s.put(key=100, val="1000")
    s[100] = "100"
    del s[0]
    for i in s:
        print(f"键{i}对应的塔高为{s.height(key=i)}") # type: ignore
    print(len(s))
    print(s.items())
    for i in s:
        print(i)