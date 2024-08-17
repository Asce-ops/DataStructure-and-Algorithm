class ArrayStack:
    '''基于数组实现的栈'''
    def __init__(self) -> None:
        '''构造方法'''
        self._stack: list[int] = [] # 用列表来模拟数组
        self._size: int = 0
    
    def __len__(self) -> int:
        '''查看栈中元素个数'''
        return self._size
    
    def push(self, item: int) -> None:
        '''入栈'''
        self._stack.append(item)
        self._size += 1

    def pop(self) -> int:
        '''出栈'''
        if self._size == 0:
            raise IndexError('栈为空')
        self._size -= 1
        return self._stack.pop()

    def peek(self) -> int:
        '''查看栈顶元素'''
        if self._size == 0:
            raise IndexError('栈为空')
        return self._stack[-1]
    
    def is_empty(self) -> bool:
        '''是否是空栈'''
        return self._size == 0
    


class Node:
    '''链表节点'''
    def __init__(self, val: int) -> None:
        '''构造方法'''
        self._val: int = val
        self._next: Node | None = None

class LinkedListStack:
    '''基于链表实现的栈'''
    def __init__(self) -> None:
        '''构造方法'''
        self._peek: Node | None = None # 头节点作为栈顶
        self._size: int = 0

    def __len__(self) -> int:
        '''查看栈中元素个数'''
        return self._size
    
    def push(self, item: int) -> None:
        '''入栈'''
        data = Node(val=item)
        data._next = self._peek
        self._peek = data
        self._size += 1
    
    def pop(self) -> int:
        '''出栈'''
        if self._peek is None:
            raise IndexError('栈为空')
        cur = self._peek
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