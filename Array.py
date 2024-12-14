from typing import Generic, TypeVar, Optional, List, override, Final

from utils import Iterator



T = TypeVar(
            name="T", 
            # covariant=True
        ) # 声明一个类型参数，不宜对其进行 type hints

class DynamicArray(Generic[T]):
    """使用列表来模拟（动态）数组"""
    capacity: Final[int] = 10 # 初始容量（不可变）
    extend_ratio: Final[int] = 2 # 每次扩容的倍数（不可变）

    def __init__(self) -> None:
        """构造方法"""
        self._capacity: int = DynamicArray.capacity # 数组容量
        print(DynamicArray.capacity)
        self._arr: List[Optional[T]] = [None] * self._capacity # 实际用于存储元素的数组
        self._size: int = 0 # 当前存储的元素数量

    def append(self, item: T) -> None:
        """在尾部追加元素
        
        Args:
            item (T): 要追加的元素
        """
        if self._size >= self._capacity: # 容量不足，扩容
            self._extend()
        self._arr[self._size] = item
        self._size += 1 # 更新元素数量

    def insert(self, idx: int, item: T) -> None:
        """在指定位置插入元素

        Args:
            idx (int): 待插入的位置
            item (T): 待插入的元素

        Raises:
            IndexError: 索引越界
        """
        if idx < 0 or idx > self._size: # 索引越界
            raise IndexError("索引越界")
        if self._size >= self._capacity: # 容量不足，扩容
            self._extend()
        for i in range(self._size, idx, -1): # 从后往前逐个移动元素
            self._arr[i] = self._arr[i-1]
        self._arr[idx] = item
        self._size += 1 # 更新元素数量

    def pop(self, idx: int = -1) -> T:
        """删除并返回指定位置的元素

        Args:
            idx (int, optional): 要删除的位置. Defaults to -1.

        Raises:
            IndexError: 索引越界

        Returns:
            T: 被删除的元素
        """
        if idx not in range(-1 * self._size, self._size): # 索引越界
            raise IndexError("索引越界")
        if idx < 0:
            idx = (idx + self._size) % self._size
        result: T = self._arr[idx] # type: ignore
        for i in range(idx, self._size - 1): # 从前往后逐个移动元素
            self._arr[i] = self._arr[i+1]
        self._arr[self._size-1] = None
        self._size -= 1 # 更新元素数量
        return result

    def remove(self, item: T) -> None:
        """删除首个指定元素

        Args:
            item (T): 待删除的元素

        Raises:
            ValueError: 待删除元素在数组中不存在
        """
        for i in range(self._size):
            if self._arr[i] == item:
                idx = i # 定位到待删除元素的位置
                # 删除元素
                for i in range(idx, self._size - 1): # 从前往后逐个移动元素
                    self._arr[i] = self._arr[i+1]
                self._arr[self._size-1] = None
                self._size -= 1 # 更新元素数量
                return
        raise ValueError(f"{item}不在数组中")
    
    def _extend(self) -> None:
        """扩容数组"""
        cur: List[T] = self._arr # type: ignore
        self._capacity *= DynamicArray.extend_ratio
        self._arr = [None] * self._capacity
        for i in range(self._size): # 将元素逐个复制到新的内存块中
            self._arr[i] = cur[i]

    def get(self, idx: int) -> T:
        """查看指定位置的元素

        Args:
            idx (int): 要查看的位置

        Raises:
            IndexError: 索引越界

        Returns:
            T: 存放在指定位置的元素
        """
        if idx not in range(-1 * self._size, self._size): # 索引越界
            raise IndexError("索引越界")
        if idx < 0:
            idx = (idx + self._size) % self._size
        return self._arr[idx] # type: ignore
    
    def set(self, idx: int, item: T) -> None:
        """修改指定位置的元素

        Args:
            idx (int): 待修改的位置
            item (T): 更新值

        Raises:
            IndexError: 索引越界
        """
        if idx not in range(-1 * self._size, self._size): # 索引越界
            raise IndexError("索引越界")
        if idx < 0:
            idx = (idx + self._size) % self._size
        self._arr[idx] = item

    def index(self, item: T) -> int:
        """查看首个指定元素的位置

        Args:
            item (T): 待查看位置的元素

        Raises:
            ValueError: 待查看元素在数组中不存在

        Returns:
            int: 待查看元素在数组中的位置
        """
        for i in range(self._size):
            if self._arr[i] == item:
                return i
        raise ValueError(f"{item}不在数组中")
    
    def __getitem__(self, idx: int) -> T:
        return self.get(idx=idx)
    
    def __setitem__(self, idx: int, item: T) -> None:
        self.set(idx=idx, item=item)

    def __len__(self) -> int:
        """获取数组的长度

        Returns:
            int: 数组长度
        """
        return self._size
    
    def getCapacity(self) -> int:
        """获取数组的当前容量

        Returns:
            int: 数组的当前容量_
        """
        return self._capacity
    
    def __contains__(self, item: T) -> bool:
        """数组中是否存在指定元素

        Args:
            item (T): 元素

        Returns:
            bool: 元素在数组中是否存在
        """
        for i in range(self._size):
            if self._arr[i] == item:
                return True
        return False
    
    def to_list(self) -> List[Optional[T]]:
        """返回列表

        Returns:
            List[Optional[T]]: 将数组中的元素以列表的形式返回
        """
        result: List[Optional[T]] = [None] * self._size
        for i in range(self._size):
            result[i] = self._arr[i]
        return result
    
    class Itr(Iterator):
        """该类配套的迭代器"""
        def __init__(self, outer: "DynamicArray[T]") -> None:
            """构造方法

            Args:
                outer (DynamicArray[T]): 指向外部类的引用
            """
            self.outer: DynamicArray[T] = outer # type: ignore
            self.cursor: int = 0

        @override
        def __next__(self) -> T:
            """实现 Iterator 接口声明的 __next__ 方法

            Raises:
                StopIteration: 停止迭代

            Returns:
                T: 
            """
            cur: int = self.cursor
            if cur >= self.outer._size:
                raise StopIteration 
            self.cursor += 1
            return self.outer._arr[cur] # type: ignore

    def __iter__(self) -> Itr:
        """使自身可迭代

        Returns:
            Itr: 类内部实现的迭代器
        """
        return self.Itr(outer=self)



if __name__ == "__main__":
    arr: DynamicArray[int] = DynamicArray[int]()
    for i in range(10):
        arr.append(item=i)
    print(arr.to_list())
    for i in arr:
        print(i)