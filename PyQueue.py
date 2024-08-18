# type: ignore

class ArrayQueue:
    '''
    基于（环形）数组实现的队列，
    使得入队和出队的时间复杂度都是O(1)
    '''
    def __init__(self) -> None:
        '''构造方法，self._queue 的有效区间段为 [self._head, self._head + self._size - 1]'''
        self._capacity: int = 10 # 队列容量
        self._queue: list[int | None] = [None] * self._capacity # 用于存储队列元素的数组
        self._head: int = 0 # 队首指针，指向队首元素
        self._size: int = 0 # 队列长度
        self._extend_ratio: int = 2 # 每次扩容的倍数

    def enqueue(self, item: int) -> None:
        '''队尾入队'''
        if self._size == self._capacity: # 扩容
            self._extend()
        tail: int = (self._head + self._size) % self._capacity # 通过取余操作实现 tail 越过数组尾部后回到头部
        self._queue[tail] = item
        self._size += 1

    def _extend(self) -> None:
        '''扩容'''
        cur = self._queue
        self._capacity *= self._extend_ratio
        self._queue = [None] * self._capacity
        for i in range(self._size): # 从队首到队尾逐个复制元素
            self._queue[i] = cur[(self._head + i) % self._size] # 触发扩容机制时 self._size 和原先的 self._capacity 相等
        self._head = 0

    def dequeue(self) -> int:
        '''队首出队'''
        if self._queue[self._head] is None: # 队列为空
            raise IndexError('队列为空')
        result = self._queue[self._head]
        self._queue[self._head] = None # 原先的队首位置元素修改为 None
        self._head = (self._head + 1) % self._capacity # 队首指针向后移动一位，若越过尾部，则返回到数组头部
        self._size -= 1
        return result
    
    def peek(self) -> int:
        '''查看队首元素'''
        if self._queue[self._head] is None: # 队列为空
            raise IndexError('队列为空')
        return self._queue[self._head]
    
    def __len__(self) -> int:
        '''查看队列长度'''
        return self._size
    
    def is_empty(self) -> bool:
        '''队列是否为空'''
        return self._queue[self._head] is None
    
    def to_list(self) -> list[int]:
        '''返回列表，头部是队首'''
        result = []
        for i in range(self._size):
            cur = self._queue[(self._head + i) % self._capacity]
            result.append(cur)
        return result
    


class Node:
    '''链表节点'''
    def __init__(self, val: int) -> None:
        '''构造方法'''
        self._val: int = val
        self._next: Node | None = None

class LinkedListQueue:
    '''基于链表实现的队列'''
    def __init__(self) -> None:
        '''构造方法'''
        self._head: Node | None = None # 头节点
        self._tail: Node | None = None # 尾节点
        self._size: int = 0 # 队列长度

    def enqueue(self, item: int) -> None:
        '''队尾入队'''
        data = Node(val=item)
        if self._head is None: # 队列为空，入队的是第一个元素
            self._head = self._tail = data
        else:
            self._tail._next = data
            self._tail = data
        self._size += 1

    def dequeue(self) -> int:
        '''队首出队'''
        if self._head is None: # 队列为空
            raise IndexError('队列为空')
        if self._head._next is None: # 出队的是队列中唯一一个元素
            self._tail = None
        result = self._head
        self._head = result._next
        result._next = None # 便于内存回收
        self._size -= 1
        return result._val
    
    def peek(self) -> int:
        '''查看队首元素'''
        if self._head is None: # 队列为空
            raise IndexError('队列为空')
        return self._head._val
    
    def __len__(self) -> int:
        '''查看队列长度'''
        return self._size
    
    def is_empty(self) -> bool:
        '''队列是否为空'''
        return self._head is None
    
    def to_list(self) -> list[int]:
        '''返回列表，头部是队首'''
        result = []
        cur = self._head
        while cur is not None:
            result.append(cur._val)
            cur = cur._next
        return result