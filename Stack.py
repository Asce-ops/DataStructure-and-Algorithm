class ArrayStack:
    '''基于数组实现的栈'''
    def __init__(self, capacity: int = 10) -> None:
        '''构造方法'''
        self._capacity: int = capacity # 栈的容量
        self._stack: list[int] = [None] * self._capacity # 用于存储栈元素的数组
        self._size: int = 0 # 栈的长度
        self._extend_ratio: int = 2 # 每次扩容的倍数

    def __len__(self) -> int:
        '''查看栈中元素个数'''
        return self._size
    
    def push(self, item: int) -> None:
        '''入栈'''
        if self._size >= self._capacity: # 扩容
            self._extend()
        self._stack[self._size] = item
        self._size += 1

    def _extend(self) -> None:
        '''扩容'''
        cur: list[int] = self._stack
        self._capacity *= self._extend_ratio
        self._stack = [None] * self._capacity
        for i in range(self._size):
            self._stack[i] = cur[i]

    def pop(self) -> int:
        '''出栈'''
        if self._size == 0:
            raise IndexError('栈为空')
        self._size -= 1
        result: int = self._stack[self._size]
        self._stack[self._size] = None
        return result

    def peek(self) -> int:
        '''查看栈顶元素'''
        if self._size == 0:
            raise IndexError('栈为空')
        return self._stack[self._size - 1]
    
    def is_empty(self) -> bool:
        '''是否是空栈'''
        return self._size == 0
    
    def to_list(self) -> list[int]:
        '''返回列表，尾部是栈顶'''
        result: list[int] = [None] * self._size
        for i in range(self._size):
            result[i] = self._stack[i]
        return result
    


class Node:
    '''链表节点'''
    def __init__(self, val: int) -> None:
        '''构造方法'''
        self._val: int = val
        self._next: Node = None

class LinkedListStack:
    '''基于链表实现的栈'''
    def __init__(self) -> None:
        '''构造方法'''
        self._peek: Node = None # 头节点作为栈顶
        self._size: int = 0

    def __len__(self) -> int:
        '''查看栈中元素个数'''
        return self._size
    
    def push(self, item: int) -> None:
        '''入栈'''
        data: Node = Node(val=item)
        data._next = self._peek
        self._peek = data
        self._size += 1
    
    def pop(self) -> int:
        '''出栈'''
        if self._peek is None:
            raise IndexError('栈为空')
        cur: Node = self._peek
        self._peek = cur._next
        cur._next = None # 便于内存回收
        self._size -= 1
        return cur._val
    
    def peek(self) -> int:
        '''查看栈顶元素'''
        if self._peek is None:
            raise IndexError('栈为空')
        return self._peek._val
    
    def is_empty(self) -> bool:
        '''是否是空栈'''
        return self._peek is None
    
    def to_list(self) -> list[int]:
        '''返回列表，尾部是栈顶'''
        result: list[int] = [None] * self._size
        cur: Node = self._peek
        idx: int = self._size - 1
        while cur is not None:
            result[idx] = cur._val
            cur = cur._next
            idx -= 1
        return result