from random import randint
from Stack import ArrayStack
from Iterator import Iterator

class HeaderNode:
    '''头节点'''
    def __init__(self) -> None:
        self._next: DataNode = None # 指向该层的首个数据节点
        self._down: HeaderNode = None # 指向下一层的头节点

class DataNode:
    '''数据节点'''
    def __init__(self, key: int, val: str) -> None:
        self._key: int = key
        self._val: str = val
        self._next: DataNode = None # 指向该层的下一个数据节点
        self._down: DataNode = None # 指向塔的下一层数据节点
        self._height: int = None # 用于记录塔高，只在每一座塔的顶层节点中不为 None

class SkipList:
    '''跳表'''
    def __init__(self) -> None:
        self._head: HeaderNode = HeaderNode() # 表头
        self._size: int = 0
    
    def search(self, key: int) -> str:
        '''查找元素'''
        cur: HeaderNode | DataNode = self._head
        while cur is not None:
            if cur._next is None: # 没有下一个数据节点则跳到下一层
                cur = cur._down
            else: # cur._next 不可能是头节点，实际上在该分支中只能是数据节点
                if key == cur._next._key: # 查找到的一定是键对应塔的最高层的数据节点
                    return cur._next._val
                elif key < cur._next._key: # 每一层是一个有序链表，此时往右的所有节点只会更大，应该降到下一层
                    cur = cur._down
                else: # key > cur._next._key
                    cur = cur._next       
        raise KeyError(f'{key}在跳表中不存在')
    
    def put(self, key: int, val: str) -> None:
        '''添加（或修改）元素'''
        cur: HeaderNode | DataNode = self._head
        stack: ArrayStack[HeaderNode | DataNode] = ArrayStack() # 要去到下一层时将当前节点入栈
        while cur is not None: # 循环结束时 cur 是第 0 层某节点 _down 的指向
            if cur._next is None:
                stack.push(item=cur)
                cur = cur._down
            else: # cur._next 不可能是头节点，实际上在该分支中只能是数据节点
                if key == cur._next._key: # 查找到的一定是键对应塔的最高层的数据节点
                    '''键存在，更新对应值'''
                    cur = cur._next
                    while cur is not None:
                        cur._val = val
                        cur = cur._down
                    return
                elif key < cur._next._key: # 每一层是一个有序链表，此时往右的所有节点只会更大，应该降到下一层
                    stack.push(item=cur)
                    cur = cur._down
                else: # key > cur._next._key
                    cur = cur._next
        '''定位到插入位置，新的键值对放在栈顶元素的后面'''
        lowest_level: HeaderNode | DataNode = stack.pop()
        data: DataNode = DataNode(key=key, val=val)
        data._next = lowest_level._next
        lowest_level._next = data
        top: DataNode = data # 塔顶
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
                prev_level: HeaderNode | DataNode = stack.pop()
                data = DataNode(key=key, val=val)
                data._down = top
                data._next = prev_level._next
                prev_level._next = data
                top = data
        top._height = height
        self._size += 1
        
    def remove(self, key: int) -> None:
        cur: HeaderNode | DataNode = self._head
        while cur is not None:
            if cur._next is None: # 没有下一个数据节点则跳到下一层
                cur = cur._down
            else:
                if key == cur._next._key: # 定位到了键所在的节点
                    '''cur 是键所在节点的前一个节点'''
                    tmp: DataNode = cur._next
                    cur._next = tmp._next
                    '''便于内存回收'''
                    tmp._next = None
                    tmp._down = None
                    while cur._down is not None: # 循环结束时已到达第 0 层
                        cur = cur._down
                        while cur._next._key != key: # 循环结束时`cur.next.key == key`
                            cur = cur._next
                        '''cur 是键所在节点的前一个节点'''
                        tmp = cur._next
                        cur._next = tmp._next
                        '''便于内存回收'''
                        tmp._next = None
                        tmp._down = None
                    self._size -= 1
                    return
                elif key < cur._next._key: # 每一层是一个有序链表，此时往右的所有节点只会更大，应该降到下一层
                    cur = cur._down
                else: # key > cur._next._key
                    cur = cur._next
        raise KeyError(f'{key}在跳表中不存在')

    def __contains__(self, key: int) -> bool:
        try:
            self.search(key=key)
            return True
        except KeyError:
            return False
    
    def __getitem__(self, key: int) -> str:
        return self.search(key=key)
    
    def __setitem__(self, key: int, val: str) -> None:
        self.put(key=key, val=val)

    def __delitem__(self, key: int) -> None:
        self.remove(key=key)

    def __len__(self) -> int:
        return self._size
    
    def keys(self) -> list[int]:
        '''查看所有键'''
        result: list[int] = [None] * self._size
        cur: HeaderNode | DataNode = self._head
        idx: int = 0
        while cur._down is not None: # 循环结束时定位到第 0 层的头节点
            cur = cur._down
        while cur._next is not None:
            result[idx] = cur._next._key
            cur = cur._next
            idx += 1
        return result
    
    def values(self) -> list[str]:
        '''查看所有值'''
        result: list[str] = [None] * self._size
        cur: HeaderNode | DataNode = self._head
        idx: int = 0
        while cur._down is not None: # 循环结束时定位到第 0 层的头节点
            cur = cur._down
        while cur._next is not None:
            result[idx] = cur._next._val
            cur = cur._next
            idx += 1
        return result
    
    def items(self) -> list[tuple[int, str]]:
        '''查看所有值'''
        result: list[tuple[int, str]] = [None] * self._size
        cur: HeaderNode | DataNode = self._head
        idx: int = 0
        while cur._down is not None: # 循环结束时定位到第 0 层的头节点
            cur = cur._down
        while cur._next is not None:
            result[idx] = (cur._next._key, cur._next._val)
            cur = cur._next
            idx += 1
        return result

    def height(self, key: int) -> int:
        '''查看指定键对应塔的塔高'''
        cur: HeaderNode | DataNode = self._head
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
        raise KeyError(f'{key}在跳表中不存在')
    
    class Itr(Iterator):
        '''该类配套的迭代器'''
        def __init__(self, outer) -> None:
            self.outer: SkipList = outer
            self.cursor: HeaderNode | DataNode = self.outer._head
            while self.cursor._down is not None: # 循环结束时定位到第 0 层的头节点
                self.cursor = self.cursor._down
            self.cursor = self.cursor._next # 定位到第 0 层的首个数据节点
        
        def __next__(self) -> int:
            '''实现 Iterator 接口声明的 __next__ 方法'''
            while self.cursor is not None:
                result: int = self.cursor._key
                self.cursor = self.cursor._next
                return result
            raise StopIteration
    def __iter__(self) -> Itr:
        return self.Itr(outer=self)



if __name__ == '__main__':
    s: SkipList = SkipList()
    for i in range(10):
        s.put(key=i, val=str(i))
    s.put(key=100, val='1000')
    s[100] = '100'
    del s[0]
    for i in s:
        print(f'键{i}对应的塔高为{s.height(key=i)}')
    print(len(s))
    print(s.items())
    for i in s:
        print(i)