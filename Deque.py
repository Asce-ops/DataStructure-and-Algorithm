from typing import Final, Generic, TypeVar, Optional, List



T = TypeVar(
            name="T", 
            # covariant=True
        ) # 声明一个类型参数，不宜对其进行 type hints

class ArrayDeque(Generic[T]):
    """基于数组实现的双端队列"""
    capacity: Final[int] = 10 # 初始容量（不可变）
    extend_ratio: Final[int] = 2 # 每次扩容的倍数（不可变）

    def __init__(self) -> None:
        """构造方法，self._deque 的有效区间段为 [self._head, self._head + self._size - 1]"""
        self._capacity: int = ArrayDeque.capacity # 队列容量
        self._deque: List[Optional[T]] = [None] * self._capacity # 用于存储队列元素的数组
        self._head: int = 0 # 队首指针，指向队首元素
        self._size: int = 0 # 队列长度

    def add_rear(self, item: T) -> None:
        """队尾入队

        Args:
            item (T): 待入队元素
        """
        if self._size == self._capacity: # 扩容
            self._extend()
        tail: int = (self._head + self._size) % self._capacity # 通过取余操作实现 tail 越过数组尾部后回到头部
        self._deque[tail] = item
        self._size += 1

    def add_front(self, item: T) -> None:
        """队首入队

        Args:
            item (T): 待入队元素
        """
        if self._size == self._capacity: # 扩容
            self._extend()
        self._head = (self._head - 1 + self._capacity) % self._capacity # 通过取余操作实现 self._head 越过数组头部后回到尾部
        self._deque[self._head] = item
        self._size += 1

    def _extend(self) -> None:
        """扩容"""
        cur: List[T] = self._deque # type: ignore
        self._capacity *= ArrayDeque.extend_ratio
        self._deque = [None] * self._capacity
        for i in range(self._size): # 从队首到队尾逐个复制元素
            self._deque[i] = cur[(self._head + i) % self._size] # 触发扩容机制时 self._size 和原先的 self._capacity 相等
        self._head = 0

    def remove_front(self) -> T:
        """队首出队

        Raises:
            IndexError: 空队列

        Returns:
            T: 出队元素
        """
        if self._deque[self._head] is None: # 队列为空
            raise IndexError("队列为空")
        result: T = self._deque[self._head] # type: ignore
        self._deque[self._head] = None # 原先的队首位置元素修改为 None
        self._head = (self._head + 1) % self._capacity # 队首指针向后移动一位，若越过尾部，则返回到数组头部
        self._size -= 1
        return result
    
    def remove_rear(self) -> T:
        """队尾出队

        Raises:
            IndexError: 空队列

        Returns:
            T: 出队元素
        """
        if self._deque[self._head] is None: # 队列为空
            raise IndexError("队列为空")
        tail: int = (self._head + self._size - 1 + self._capacity) % self._capacity
        result: T = self._deque[tail] # type: ignore
        self._deque[tail] = None # 原先的队尾位置元素修改为 None
        self._size -= 1
        return result
    
    def peek_front(self) -> T:
        """查看队首元素

        Raises:
            IndexError: 空队列

        Returns:
            T: 队首元素
        """
        if self._deque[self._head] is None: # 队列为空
            raise IndexError("队列为空")
        return self._deque[self._head] # type: ignore
    
    def peek_rear(self) -> T:
        """查看队尾元素

        Raises:
            IndexError: 空队列

        Returns:
            T: 队尾元素
        """
        if self._deque[self._head] is None: # 队列为空
            raise IndexError("队列为空")
        tail: int = (self._head + self._size - 1 + self._capacity) % self._capacity
        return self._deque[tail] # type: ignore
    
    def __len__(self) -> int:
        """查看队列长度

        Returns:
            int: 队列中元素数量
        """
        return self._size
    
    def is_empty(self) -> bool:
        """队列是否为空

        Returns:
            bool: 队列是否为空
        """
        return self._deque[self._head] is None
    
    def to_list(self) -> List[T]:
        """返回列表（头部是队首）

        Returns:
            List[T]: 将队列中的元素以列表的形式返回
        """
        result: List[Optional[T]] = [None] * self._size
        for i in range(self._size):
            cur: T = self._deque[(self._head + i) % self._capacity] # type: ignore
            result[i] = cur
        return result # type: ignore
    


class Node(Generic[T]):
    """双向链表节点"""
    def __init__(self, val: T) -> None:
        """构造方法

        Args:
            val (T): 节点中存储的元素
        """
        self._val: T = val
        self._next: Optional[Node[T]] = None
        self._prev: Optional[Node[T]] = None # 便于从队尾出队

class LinkedListDeque(Generic[T]):
    """基于双向链表实现的双端队列"""
    def __init__(self) -> None:
        """构造方法"""
        self._head: Optional[Node[T]] = None # 头节点
        self._tail: Optional[Node[T]] = None # 尾节点
        self._size: int = 0 # 队列长度

    def add_rear(self, item: T) -> None:
        """队尾入队

        Args:
            item (T): 待入队元素
        """
        data: Node[T] = Node[T](val=item)
        if self._head is None: # 队列为空，入队的是第一个元素
            self._head = self._tail = data
        else:
            self._tail._next = data # type: ignore
            data._prev = self._tail
            self._tail = data
        self._size += 1

    def add_front(self, item: T) -> None:
        """队首入队

        Args:
            item (T): 待入队元素
        """
        data: Node[T] = Node[T](val=item)
        if self._head is None: # 队列为空，入队的是第一个元素
            self._head = self._tail = data
        else:
            self._head._prev = data
            data._next = self._head
            self._head = data
        self._size += 1

    def remove_front(self) -> T:
        """队首出队

        Raises:
            IndexError: 空队列

        Returns:
            T: 出队元素
        """
        if self._head is None: # 队列为空
            raise IndexError("队列为空")
        elif self._head._next is None: # 出队的是队列中唯一一个元素
            self._tail = None
            result: Node[T] = self._head
            self._head = None
        else:
            result: Node[T] = self._head
            self._head = result._next
            self._head._prev = None # type: ignore
            result._next = None # 便于内存回收
        self._size -= 1
        return result._val
    
    def remove_rear(self) -> T:
        """队尾出队

        Raises:
            IndexError: 空队列

        Returns:
            T: 出队元素
        """
        if self._head is None: # 队列为空
            raise IndexError("队列为空")
        elif self._tail._prev is None: # type: ignore # 出队的是队列中唯一一个元素
            self._head = None
            result: Node[T] = self._tail # type: ignore
            self._tail = None
        else:
            result: Node[T] = self._tail # type: ignore
            self._tail = result._prev
            self._tail._next = None # type: ignore
            result._prev = None # 便于内存回收
        self._size -= 1
        return result._val
    
    def peek_front(self) -> T:
        """查看队首元素

        Raises:
            IndexError: 空队列

        Returns:
            T: 队首元素
        """
        if self._head is None: # 队列为空
            raise IndexError("队列为空")
        return self._head._val
    
    def peek_rear(self) -> T:
        """查看队尾元素

        Raises:
            IndexError: 空队列

        Returns:
            T: 队尾元素
        """
        if self._head is None: # 队列为空
            raise IndexError("队列为空")
        return self._tail._val # type: ignore
    
    def __len__(self) -> int:
        """查看队列长度

        Returns:
            int: 队列中元素数量
        """
        return self._size
    
    def is_empty(self) -> bool:
        """队列是否为空

        Returns:
            bool: 队列是否为空
        """
        return self._head is None
    
    def to_list(self) -> List[T]:
        """返回列表（头部是队首）

        Returns:
            List[T]: 将队列中的元素以列表的形式返回
        """
        result: List[Optional[T]] = [None] * self._size
        cur: Optional[Node[T]] = self._head
        idx: int = 0
        while cur is not None:
            result[idx] = cur._val
            idx += 1
            cur = cur._next
        return result # type: ignore



if __name__ == "__main__":
    deque1: ArrayDeque[str] = ArrayDeque[str]()
    deque2: LinkedListDeque[str] = LinkedListDeque[str]()
    for string in ["a", "b", "c", "d"]:
        deque1.add_front(item=string)
        deque2.add_front(item=string)
    for string in ["A", "B", "C", "D"]:
        deque1.add_rear(item=string)
        deque2.add_rear(item=string)
    print(deque1.remove_front(), deque2.remove_front())
    print(deque1.remove_rear(), deque2.remove_rear())
    print(deque1.to_list(), deque2.to_list())