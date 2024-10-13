# type: ignore

class ArrayDeque:
    '''基于数组实现的双端队列'''
    def __init__(self, capacity: int = 10) -> None:
        '''构造方法，self._deque 的有效区间段为 [self._head, self._head + self._size - 1]'''
        self._capacity: int = capacity # 队列容量
        self._deque: list[int] = [None] * self._capacity # 用于存储队列元素的数组
        self._head: int = 0 # 队首指针，指向队首元素
        self._size: int = 0 # 队列长度
        self._extend_ratio: int = 2 # 每次扩容的倍数

    def add_rear(self, item: int) -> None:
        '''队尾入队'''
        if self._size == self._capacity: # 扩容
            self._extend()
        tail: int = (self._head + self._size) % self._capacity # 通过取余操作实现 tail 越过数组尾部后回到头部
        self._deque[tail] = item
        self._size += 1

    def add_front(self, item: int) -> None:
        '''队首入队'''
        if self._size == self._capacity: # 扩容
            self._extend()
        self._head = (self._head - 1 + self._capacity) % self._capacity # 通过取余操作实现 self._head 越过数组头部后回到尾部
        self._deque[self._head] = item
        self._size += 1

    def _extend(self) -> None:
        '''扩容'''
        cur: list[int] = self._deque
        self._capacity *= self._extend_ratio
        self._deque = [None] * self._capacity
        for i in range(self._size): # 从队首到队尾逐个复制元素
            self._deque[i] = cur[(self._head + i) % self._size] # 触发扩容机制时 self._size 和原先的 self._capacity 相等
        self._head = 0

    def remove_front(self) -> int:
        '''队首出队'''
        if self._deque[self._head] is None: # 队列为空
            raise IndexError('队列为空')
        result: int = self._deque[self._head]
        self._deque[self._head] = None # 原先的队首位置元素修改为 None
        self._head = (self._head + 1) % self._capacity # 队首指针向后移动一位，若越过尾部，则返回到数组头部
        self._size -= 1
        return result
    
    def remove_rear(self) -> int:
        '''队尾出队'''
        if self._deque[self._head] is None: # 队列为空
            raise IndexError('队列为空')
        tail: int = (self._head + self._size - 1 + self._capacity) % self._capacity
        result: int = self._deque[tail]
        self._deque[tail] = None # 原先的队尾位置元素修改为 None
        self._size -= 1
        return result
    
    def peek_front(self) -> int:
        '''查看队首元素'''
        if self._deque[self._head] is None: # 队列为空
            raise IndexError('队列为空')
        return self._deque[self._head]
    
    def peek_rear(self) -> int:
        '''查看队尾元素'''
        if self._deque[self._head] is None: # 队列为空
            raise IndexError('队列为空')
        tail: int = (self._head + self._size - 1 + self._capacity) % self._capacity
        return self._deque[tail]
    
    def __len__(self) -> int:
        '''查看队列长度'''
        return self._size
    
    def is_empty(self) -> bool:
        '''队列是否为空'''
        return self._deque[self._head] is None
    
    def to_list(self) -> list[int]:
        '''返回列表，头部是队首'''
        result: list[int] = [None] * self._size
        for i in range(self._size):
            cur: int = self._deque[(self._head + i) % self._capacity]
            result[i] = cur
        return result
    


class Node:
    '''双向链表节点'''
    def __init__(self, val: int) -> None:
        '''构造方法'''
        self._val: int = val
        self._next: Node = None
        self._prev: Node = None # 便于从队尾出队

class LinkedListDeque:
    '''基于双向链表实现的双端队列'''
    def __init__(self) -> None:
        '''构造方法'''
        self._head: Node = None # 头节点
        self._tail: Node = None # 尾节点
        self._size: int = 0 # 队列长度

    def add_rear(self, item: int) -> None:
        '''队尾入队'''
        data: Node = Node(val=item)
        if self._head is None: # 队列为空，入队的是第一个元素
            self._head = self._tail = data
        else:
            self._tail._next = data
            data._prev = self._tail
            self._tail = data
        self._size += 1

    def add_front(self, item: int) -> None:
        '''队首入队'''
        data: Node = Node(val=item)
        if self._head is None: # 队列为空，入队的是第一个元素
            self._head = self._tail = data
        else:
            self._head._prev = data
            data._next = self._head
            self._head = data
        self._size += 1

    def remove_front(self) -> int:
        '''队首出队'''
        if self._head is None: # 队列为空
            raise IndexError('队列为空')
        elif self._head._next is None: # 出队的是队列中唯一一个元素
            self._tail = None
            result: Node = self._head
            self._head = None
        else:
            result: Node = self._head
            self._head = result._next
            self._head._prev = None
            result._next = None # 便于内存回收
        self._size -= 1
        return result._val
    
    def remove_rear(self) -> int:
        '''队尾出队'''
        if self._head is None: # 队列为空
            raise IndexError('队列为空')
        elif self._tail._prev is None: # 出队的是队列中唯一一个元素
            self._head = None
            result: Node = self._tail
            self._tail = None
        else:
            result: Node = self._tail
            self._tail = result._prev
            self._tail._next = None
            result._prev = None # 便于内存回收
        self._size -= 1
        return result._val
    
    def peek_front(self) -> int:
        '''查看队首元素'''
        if self._head is None: # 队列为空
            raise IndexError('队列为空')
        return self._head._val
    
    def peek_rear(self) -> int:
        '''查看队首元素'''
        if self._head is None: # 队列为空
            raise IndexError('队列为空')
        return self._tail._val
    
    def __len__(self) -> int:
        '''查看队列长度'''
        return self._size
    
    def is_empty(self) -> bool:
        '''队列是否为空'''
        return self._head is None
    
    def to_list(self) -> list[int]:
        '''返回列表，头部是队首'''
        result: list[int] = [None] * self._size
        cur: Node = self._head
        idx: int = 0
        while cur is not None:
            result[idx] = cur._val
            idx += 1
            cur = cur._next
        return result