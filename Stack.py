from typing import Final, Generic, TypeVar, Optional, List



T = TypeVar(
            name="T", 
            # covariant=True
        ) # 声明一个类型参数，不宜对其进行 type hints

class ArrayStack(Generic[T]):
    """基于数组实现的栈"""
    capacity: Final[int] = 10 # 初始容量（不可变）
    extend_ratio: Final[int] = 2 # 每次扩容的倍数（不可变）

    def __init__(self) -> None:
        """构造方法"""
        self._capacity: int = ArrayStack.capacity # 栈的容量
        self._stack: List[Optional[T]] = [None] * self._capacity # 用于存储栈元素的数组
        self._size: int = 0 # 栈的长度

    def __len__(self) -> int:
        """查看栈中元素数量

        Returns:
            int: 栈中存储的元素数量
        """
        return self._size
    
    def push(self, item: T) -> None:
        """入栈

        Args:
            item (T): 待入栈元素
        """
        if self._size >= self._capacity: # 扩容
            self._extend()
        self._stack[self._size] = item
        self._size += 1

    def _extend(self) -> None:
        """扩容"""
        cur: List[T] = self._stack # type: ignore
        self._capacity *= ArrayStack.extend_ratio
        self._stack = [None] * self._capacity
        for i in range(self._size):
            self._stack[i] = cur[i]

    def pop(self) -> T:
        """出栈

        Raises:
            IndexError: 空栈

        Returns:
            T: 出栈元素
        """
        if self._size == 0:
            raise IndexError("栈为空")
        self._size -= 1
        result: T = self._stack[self._size] # type: ignore
        self._stack[self._size] = None
        return result

    def peek(self) -> T:
        """查看栈顶元素

        Raises:
            IndexError: 空栈

        Returns:
            T: 栈顶元素
        """
        if self._size == 0:
            raise IndexError("栈为空")
        return self._stack[self._size - 1] # type: ignore
    
    def is_empty(self) -> bool:
        """是否是空栈

        Returns:
            bool: 是否是空栈
        """
        return self._size == 0
    
    def to_list(self) -> List[T]:
        """返回列表（尾部是栈顶）

        Returns:
            List[T]: 将栈中的元素以列表的形式返回
        """
        result: List[Optional[T]] = [None] * self._size
        for i in range(self._size):
            result[i] = self._stack[i]
        return result # type: ignore
    


class Node(Generic[T]):
    """链表节点"""
    def __init__(self, val: T) -> None:
        """构造方法

        Args:
            val (T): 节点中存储的元素
        """
        self._val: T = val
        self._next: Optional[Node] = None

class LinkedListStack(Generic[T]):
    """基于链表实现的栈"""
    def __init__(self) -> None:
        """构造方法"""
        self._peek: Optional[Node[T]] = None # 头节点作为栈顶
        self._size: int = 0

    def __len__(self) -> int:
        """查看栈中元素数量

        Returns:
            int: 栈中存储的元素数量
        """
        return self._size
    
    def push(self, item: T) -> None:
        """入栈

        Args:
            item (T): 待入栈元素
        """
        data: Node[T] = Node[T](val=item)
        data._next = self._peek
        self._peek = data
        self._size += 1
    
    def pop(self) -> T:
        """出栈

        Raises:
            IndexError: 空栈

        Returns:
            T: 出栈元素
        """
        if self._peek is None:
            raise IndexError("栈为空")
        cur: Node[T] = self._peek
        self._peek = cur._next
        cur._next = None # 便于内存回收
        self._size -= 1
        return cur._val
    
    def peek(self) -> T:
        """查看栈顶元素

        Raises:
            IndexError: 空栈

        Returns:
            T: 栈顶元素
        """
        if self._peek is None:
            raise IndexError("栈为空")
        return self._peek._val
    
    def is_empty(self) -> bool:
        """是否是空栈

        Returns:
            bool: 是否是空栈
        """
        return self._peek is None
    
    def to_list(self) -> List[T]:
        """返回列表（尾部是栈顶）

        Returns:
            List[T]: 将栈中的元素以列表的形式返回
        """
        result: List[Optional[T]] = [None] * self._size
        cur: Optional[Node[T]] = self._peek
        idx: int = self._size - 1
        while cur is not None:
            result[idx] = cur._val
            cur = cur._next
            idx -= 1
        return result # type: ignore



if __name__ == "__main__":
    stack1: ArrayStack[str] = ArrayStack[str]()
    stack2: LinkedListStack[str] = LinkedListStack[str]()
    for string in ["a", "b", "c"]:
        stack1.push(item=string)
        stack2.push(item=string)
    print(stack1.pop(), stack2.pop())
    print(stack1.to_list(), stack2.to_list())