from typing import Generic, TypeVar, Optional, List, override

from utils import Iterator



T = TypeVar(
            name="T", 
            # covariant=True
        ) # 声明一个类型参数，不宜对其进行 type hints

class ListNode(Generic[T]):
    """链表的节点"""
    def __init__(self, val: T) -> None:
        """构造方法

        Args:
            val (T): 节点中存储的元素
        """
        self._val: T = val # 节点实际存储的数据
        self._next: Optional[ListNode[T]] = None # 指向下一个节点的引用

class LinkedList(Generic[T]):
    """链表"""
    def __init__(self) -> None:
        """构造方法"""
        self._head: Optional[ListNode[T]] = None # 头结点
        self._tail: Optional[ListNode[T]] = None # 尾节点，便于追加元素
        self._size: int = 0

    def append(self, val: T) -> None:
        """在链表的尾部追加元素

        Args:
            val (T): 待追加的元素
        """
        data: ListNode[T] = ListNode[T](val=val)
        if self._head is None: # 添加第一个元素
            self._head = self._tail = data
        else:
            self._tail._next = data # type: ignore
            self._tail = data
        self._size += 1

    def insert(self, idx: int, val: T) -> None:
        """在指定位置插入元素

        Args:
            idx (int): 待插入的位置
            val (T): 待插入元素

        Raises:
            IndexError: 索引越界
        """
        if idx < 0 or idx > self._size:
            raise IndexError("索引越界")
        data: ListNode[T] = ListNode[T](val=val)
        if idx == 0: # 在头部插入，需要修改头节点
            if self._head is None: # 插入的是第一个元素
                self._head = self._tail = data
            else:
                data._next = self._head
                self._head = data
        elif idx == self._size: # 在尾部插入，需要修改尾节点
            self._tail._next = data # type: ignore
            self._tail = data
        else: # 无需修改头结点或尾节点
            cur: ListNode[T] = self._head # type: ignore
            for _ in range(idx - 1): # 定位到指定位置的前一个位置
                cur = cur._next # type: ignore
            data._next = cur._next
            cur._next = data
        self._size += 1
    
    def pop(self, idx: int = -1) -> T:
        """删除并返回指定位置的元素

        Args:
            idx (int, optional): 要删除的位置. Defaults to -1.

        Raises:
            IndexError: 索引越界

        Returns:
            T: 被删除的元素
        """
        if idx < -1 * self._size or idx >= self._size: # 索引越界（含 self._head is None 的情况）
            raise IndexError("索引越界")
        if idx < 0:
            idx = (idx + self._size) % self._size
        if idx == 0: # 删除的是第一个元素，需要修改头节点
            result: ListNode[T] = self._head # type: ignore
            if result._next is None: # 删除的是唯一一个元素
                self._head = self._head = None
            else:
                self._head = result._next
                result._next = None # 使得删除的节点不再和链表关联，便于内存回收
        else:
            cur: ListNode[T] = self._head # type: ignore
            for _ in range(idx - 1): # 定位到指定位置的前一个位置
                cur = cur._next # type: ignore
            result: ListNode[T] = cur._next # type: ignore
            if result._next is None: # 删除的是最后一个位置的元素，需修改尾节点
                cur._next = None
                self._tail = cur
            else: # 无需修改头结点或尾节点
                cur._next = result._next
                result._next = None # 使得删除的节点不再和链表关联，便于内存回收
        self._size -= 1
        return result._val
    
    def remove(self, val: T) -> None:
        """删除首个指定元素

        Args:
            val (T): 待删除元素

        Raises:
            ValueError: 链表为空
            ValueError: 待删除元素不在链表中
        """
        if self._head is None: # 链表为空
            raise ValueError("链表为空")
        if self._head._val == val: # 要删除的是第一个元素
            tmp: ListNode[T] = self._head
            if tmp._next is None: # 要删除的是唯一一个元素
                self._head = self._tail = None
            else:
                self._head = tmp._next
                tmp._next = None
            self._size -= 1
        else:
            cur: ListNode[T] = self._head
            while cur._next is not None:
                if cur._next._val == val: # 定位到待删除元素的前一个位置
                    tmp: ListNode[T] = cur._next # 待删除元素的位置
                    if tmp._next is None: # 待删除元素是最后一个元素
                        cur._next = None
                        self._tail = cur
                    else:
                        cur._next = tmp._next
                        tmp._next = None
                    self._size -= 1
                    return
                cur = cur._next
            raise ValueError(f"{val}不在链表中")
        
    def get(self, idx: int) -> T:
        """查看指定位置的元素

        Args:
            idx (int): 待查看的位置

        Raises:
            IndexError: 索引越界

        Returns:
            T: 指定位置上的元素
        """
        if idx < -1 * self._size or idx >= self._size: # 索引越界
            raise IndexError("索引越界")
        if idx == 0: # 头结点无需遍历可直接访问
            return self._head._val # type: ignore
        elif idx == -1: # 尾结点无需遍历可直接访问
            return self._tail._val # type: ignore
        else:
            if idx < 0:
                idx = (idx + self._size) % self._size
            cur: ListNode[T] = self._head # type: ignore
            for _ in range(idx):
                cur = cur._next # type: ignore
            return cur._val
        
    def set(self, idx: int, val: T) -> None:
        """修改指定位置的元素

        Args:
            idx (int): 待修改的位置
            val (T): 更新值

        Raises:
            IndexError: 索引越界
        """
        if idx < -1 * self._size or idx >= self._size: # 索引越界
            raise IndexError("索引越界")
        if idx == 0: # 头结点无需遍历可直接访问
            self._head._val = val # type: ignore
        elif idx == -1: # 尾结点无需遍历可直接访问
            self._tail._val = val # type: ignore
        else:
            if idx < 0:
                idx = (idx + self._size) % self._size
            cur: ListNode[T] = self._head # type: ignore
            for _ in range(idx):
                cur = cur._next # type: ignore
            cur._val = val

    def __getitem__(self, idx: int) -> T:
        """查看指定位置的元素

        Args:
            idx (int): 待查看的位置

        Returns:
            T: 指定位置上的元素
        """
        return self.get(idx=idx)
    
    def __setitem__(self, idx: int, val: T) -> None:
        """修改指定位置的元素

        Args:
            idx (int): 待修改的位置
            val (T): 更新值
        """
        self.set(idx=idx, val=val)

    def __len__(self) -> int:
        """查看链表长度

        Returns:
            int: 链表长度
        """
        return self._size
    
    def __contains__(self, val: T) -> bool:
        """链表中是否存在指定元素

        Args:
            val (T): 元素

        Returns:
            bool: 元素在链表中是否存在
        """
        cur: Optional[ListNode[T]] = self._head
        while cur is not None:
            if cur._val == val:
                return True
            cur = cur._next
        return False
    
    def index(self, val: T) -> int:
        """查看首个指定元素的位置

        Args:
            val (T): _description_

        Raises:
            ValueError: 空链表
            ValueError: 待查看元素在链表中不存在

        Returns:
            int: 待查看元素在链表中的位置
        """
        if self._head is None: # 链表为空
            raise ValueError("空链表")
        cur: Optional[ListNode[T]] = self._head
        idx: int = 0
        while cur is not None:
            if cur._val == val:
                return idx
            cur = cur._next
            idx += 1
        raise ValueError(f"{val}不在链表中")
    
    def to_list(self) -> List[T]:
        """返回列表（左端是头节点）

        Returns:
            List[Optional[T]]: 将链表中的元素以列表的形式返回
        """
        result: List[Optional[T]] = [None] * self._size
        cur: Optional[ListNode[T]] = self._head
        idx: int = 0
        while cur is not None:
            result[idx] = cur._val
            cur = cur._next
            idx += 1
        return result # type: ignore

    class Itr(Iterator):
        """该类配套的迭代器"""
        def __init__(self, outer: "LinkedList[T]") -> None:
            """构造方法

            Args:
                outer (LinkedList[T]): 指向外部类的引用
            """
            self.outer: LinkedList[T] = outer # type: ignore
            self.cursor: Optional[ListNode] = self.outer._head

        @override
        def __next__(self) -> T:
            """实现 Iterator 接口声明的 __next__ 方法

            Raises:
                StopIteration: 停止迭代

            Returns:
                T: 
            """
            cur: Optional[ListNode[T]] = self.cursor # type: ignore
            if cur is None:
                raise StopIteration
            self.cursor = self.cursor._next # type: ignore
            return cur._val

    def __iter__(self) -> Itr:
        """使自身可迭代

        Returns:
            Itr: 类内部实现的迭代器
        """
        return self.Itr(outer=self)



if __name__ == "__main__":
    l: LinkedList[int] = LinkedList[int]()
    for i in range(10):
        l.append(val=i)
    print(l.to_list())
    for i in l:
        print(i)