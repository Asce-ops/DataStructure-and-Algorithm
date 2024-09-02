# type: ignore

class ListNode:
    '''链表的节点'''
    def __init__(self, val: int) -> None:
        '''构造方法'''
        self._val: int = val # 节点实际存储的数据
        self._next: ListNode | None = None # 指向下一个节点的引用

class LinkedList:
    '''链表'''
    def __init__(self) -> None:
        '''构造方法'''
        self._head: ListNode | None = None # 头结点
        self._tail: ListNode | None = None # 尾节点，便于追加元素
        self._size: int = 0

    def append(self, val: int) -> None:
        '''在链表的尾部追加元素'''
        data = ListNode(val=val)
        if self._head is None: # 添加第一个元素
            self._head = self._tail = data
        else:
            self._tail._next = data
            self._tail = data
        self._size += 1

    def insert(self, idx: int, val: int) -> None:
        '''在指定位置插入元素'''
        if idx < 0 or idx > self._size:
            raise IndexError('索引越界')
        data = ListNode(val=val)
        if idx == 0: # 在头部插入，需要修改头结点
            if self._head is None: # 插入的是第一个元素
                self._head = self._tail = data
            else:
                data._next = self._head
                self._head = data
        elif idx == self._size: # 在尾部插入，需要修改尾节点
            self._tail._next = data
            self._tail = data
        else: # 无需修改头结点或尾节点
            cur = self._head
            for _ in range(idx - 1): # 定位到指定位置的前一个位置
                cur = cur._next
            data._next = cur._next
            cur._next = data
        self._size += 1
    
    def pop(self, idx: int = -1) -> int:
        '''删除并返回指定位置的元素'''
        if idx < -1 * self._size or idx >= self._size: # 索引越界
            raise IndexError('索引越界')
        if idx < 0:
            idx = (idx + self._size) % self._size
        if idx == 0: # 删除的是第一个元素，需要修改头节点
            result = self._head
            if result._next is None: # 删除的是唯一一个元素
                self._head = self._head = None
            else:
                self._head = result._next
                result._next = None # 使得删除的节点不再和链表关联，便于内存回收
        else:
            cur = self._head
            for _ in range(idx - 1): # 定位到指定位置的前一个位置
                cur = cur._next
            result = cur._next
            if result._next is None: # 删除的是最后一个位置的元素，需修改尾节点
                cur._next = None
                self._tail = cur
            else: # 无需修改头结点或尾节点
                cur._next = result._next
                result._next = None # 使得删除的节点不再和链表关联，便于内存回收
        self._size -= 1
        return result._val
    
    def remove(self, val: int) -> None:
        '''删除首个指定元素'''
        if self._head is None: # 链表为空
            raise ValueError(f'{val}不在链表中')
        if self._head._val == val: # 要删除的是第一个元素
            tmp = self._head
            if tmp._next is None: # 要删除的是唯一一个元素
                self._head = self._tail = None
            else:
                self._head = tmp._next
                tmp._next = None
            self._size -= 1
        else:
            cur = self._head
            while cur._next is not None:
                if cur._next._val == val: # 定位到待删除元素的前一个位置
                    tmp = cur._next # 待删除元素的位置
                    if tmp._next is None: # 待删除元素是最后一个元素
                        cur._next = None
                        self._tail = cur
                    else:
                        cur._next = tmp._next
                        tmp._next = None
                    self._size -= 1
                    return
                cur = cur._next
            raise ValueError(f'{val}不在链表中')
        
    def get(self, idx: int) -> int:
        '''查看指定位置的元素'''
        if idx < -1 * self._size or idx >= self._size: # 索引越界
            raise IndexError('索引越界')
        if idx == 0: # 头结点无需遍历可直接访问
            return self._head._val
        elif idx == -1: # 尾结点无需遍历可直接访问
            return self._tail._val
        else:
            if idx < 0:
                idx = (idx + self._size) % self._size
            cur = self._head
            for _ in range(idx):
                cur = cur._next
            return cur._val
        
    def set(self, idx: int, val: int) -> None:
        '''修改指定位置的元素'''
        if idx < -1 * self._size or idx >= self._size: # 索引越界
            raise IndexError('索引越界')
        if idx == 0: # 头结点无需遍历可直接访问
            self._head._val = val
        elif idx == -1: # 尾结点无需遍历可直接访问
            self._tail._val = val
        else:
            if idx < 0:
                idx = (idx + self._size) % self._size
            cur = self._head
            for _ in range(idx):
                cur = cur._next
            cur._val = val

    def __getitem__(self, idx: int) -> int:
        return self.get(idx=idx)
    
    def __setitem__(self, idx: int, val: int) -> None:
        self.set(idx=idx, val=val)

    def __len__(self) -> int:
        '''查看链表长度'''
        return self._size
    
    def __contains__(self, val: int) -> bool:
        '''链表中是否存在指定元素'''
        cur = self._head
        while cur is not None:
            if cur._val == val:
                return True
            cur = cur._next
        return False
    
    def index(self, val: int) -> int:
        '''查看首个指定元素的位置'''
        if self._head is None: # 链表为空
            raise ValueError(f'{val}不在链表中')
        cur, idx = self._head, 0
        while cur is not None:
            if cur._val == val:
                return idx
            cur = cur._next
            idx += 1
        raise ValueError(f'{val}不在链表中')
    
    def to_list(self) -> list[int]:
        '''返回列表，左端是头节点'''
        result = [None] * self._size
        cur = self._head
        idx = 0
        while cur is not None:
            result[idx] = cur._val
            cur = cur._next
            idx += 1
        return result
    
    def __iter__(self):
        '''使自身可迭代'''
        self.__tmp: ListNode | None = self._head
        return self
    
    def __next__(self) -> int:
        '''迭代自身'''
        cur = self.__tmp
        if cur is None:
            raise StopIteration
        self.__tmp = self.__tmp._next
        return cur._val