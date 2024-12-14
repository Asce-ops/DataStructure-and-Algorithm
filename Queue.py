from typing import Final, Generic, TypeVar, Optional, List



T = TypeVar(
            name="T", 
            # covariant=True
        ) # 声明一个类型参数，不宜对其进行 type hints

class ArrayQueue(Generic[T]):
    """
    基于（环形）数组实现的队列，
    使得入队和出队的时间复杂度都是O(1)
    """
    capacity: Final[int] = 10 # 初始容量（不可变）
    extend_ratio: Final[int] = 2 # 每次扩容的倍数（不可变）

    def __init__(self) -> None:
        """构造方法，self._queue 的有效区间段为 [self._head, self._head + self._size - 1]"""
        self._capacity: int = ArrayQueue.capacity # 队列容量
        self._queue: List[Optional[T]] = [None] * self._capacity # 用于存储队列元素的数组
        self._head: int = 0 # 队首指针，指向队首元素
        self._size: int = 0 # 队列长度

    def enqueue(self, item: T) -> None:
        """队尾入队

        Args:
            item (T): 待入队元素
        """
        if self._size == self._capacity: # 扩容
            self._extend()
        tail: int = (self._head + self._size) % self._capacity # 通过取余操作实现 tail 越过数组尾部后回到头部
        self._queue[tail] = item
        self._size += 1

    def _extend(self) -> None:
        """扩容"""
        cur: List[T] = self._queue # type: ignore
        self._capacity *= ArrayQueue.extend_ratio
        self._queue = [None] * self._capacity
        for i in range(self._size): # 从队首到队尾逐个复制元素
            self._queue[i] = cur[(self._head + i) % self._size] # 触发扩容机制时 self._size 和原先的 self._capacity 相等
        self._head = 0

    def dequeue(self) -> T:
        """队首出队

        Raises:
            IndexError: 空队列

        Returns:
            T: 出队元素
        """
        if self._queue[self._head] is None: # 队列为空
            raise IndexError("队列为空")
        result: T = self._queue[self._head] # type: ignore
        self._queue[self._head] = None # 原先的队首位置元素修改为 None
        self._head = (self._head + 1) % self._capacity # 队首指针向后移动一位，若越过尾部，则返回到数组头部
        self._size -= 1
        return result
    
    def peek(self) -> T:
        """查看队首元素

        Raises:
            IndexError: 空队列

        Returns:
            T: 队首元素
        """
        if self._queue[self._head] is None: # 队列为空
            raise IndexError("队列为空")
        return self._queue[self._head] # type: ignore
    
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
        return self._queue[self._head] is None
    
    def to_list(self) -> List[T]:
        """返回列表（头部是队首）

        Returns:
            List[T]: 将队列中的元素以列表的形式返回
        """
        result: List[Optional[T]] = [None] * self._size
        for i in range(self._size):
            cur: T = self._queue[(self._head + i) % self._capacity] # type: ignore
            result[i] = cur
        return result # type: ignore



class Node(Generic[T]):
    """链表节点"""
    def __init__(self, val: T) -> None:
        """构造方法

        Args:
            val (T): 节点中存储的元素
        """
        self._val: T = val
        self._next: Optional[Node[T]] = None

class LinkedListQueue(Generic[T]):
    """基于链表实现的队列"""
    def __init__(self) -> None:
        """构造方法"""
        self._head: Optional[Node[T]] = None # 头节点
        self._tail: Optional[Node[T]] = None # 尾节点
        self._size: int = 0 # 队列长度

    def enqueue(self, item: T) -> None:
        """队尾入队

        Args:
            item (T): 待入队元素
        """
        data: Node[T] = Node[T](val=item)
        if self._head is None: # 队列为空，入队的是第一个元素
            self._head = self._tail = data
        else:
            self._tail._next = data # type: ignore
            self._tail = data
        self._size += 1

    def dequeue(self) -> T:
        """队首出队

        Raises:
            IndexError: 空队列

        Returns:
            T: 出队元素
        """
        if self._head is None: # 队列为空
            raise IndexError("队列为空")
        if self._head._next is None: # 出队的是队列中唯一一个元素
            self._tail = None
        result: Node[T] = self._head
        self._head = result._next
        result._next = None # 便于内存回收
        self._size -= 1
        return result._val
    
    def peek(self) -> T:
        """查看队首元素

        Raises:
            IndexError: 空队列

        Returns:
            T: 队首元素
        """
        if self._head is None: # 队列为空
            raise IndexError("队列为空")
        return self._head._val
    
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
    queue1: ArrayQueue[str] = ArrayQueue[str]()
    queue2: LinkedListQueue[str] = LinkedListQueue[str]()
    for string in ["a", "b", "c"]:
        queue1.enqueue(item=string)
        queue2.enqueue(item=string)
    print(queue1.dequeue(), queue2.dequeue())
    print(queue1.to_list(), queue2.to_list())