from typing import Final, Generic, TypeVar, Optional, List, Sequence, override

from utils import Comparable



K = TypeVar(name="K", bound=Comparable) # 声明一个类型参数，不宜对其进行 type hints
V = TypeVar(
            name="V", 
            # covariant=True
        )

class MaxHeap(Generic[K]):
    """大顶堆（完全二叉树，任意非叶子节点的值大于等于其子节点的值）"""
    extend_ratio: Final[int] = 2 # 每次扩容的倍数（不可变）

    def __init__(self, data: Optional[Sequence[K]] = None) -> None:
        """构造方法

        Args:
            data (Optional[Sequence[K]], optional): 待堆化的序列. Defaults to None.
        """
        self._heap: List[Optional[K]]
        self._capacity: int # 容量
        self._size: int
        if data is None: # 初始化一个空堆
            self._capacity = 10
            self._heap = [None] * self._capacity
            self._size = 0
        else: # 堆化现有数组（非原地）
            self._capacity = len(data)
            self._heap = [None] * self._capacity
            self._size = self._capacity
            last_not_leaf: int = (self._size - 2) // 2 # 最后一个非叶子节点（有可能等于-1）
            for i in range(last_not_leaf + 1, self._size):
                self._heap[i] = data[i]
            for i in range(last_not_leaf, -1, -1):
                # 倒序遍历数组（层序遍历的倒序），依次对每个非叶节点执行“从顶至底堆化”；
                # 每当堆化一个节点后，以该节点为根节点的子树就形成一个合法的子堆。
                self._heap[i] = data[i]
                self._sift_down(idx=i)

    def _extend(self) -> None:
        """扩容"""
        tmp: List[K] = self._heap # type: ignore
        self._capacity *= self.extend_ratio
        self._heap = [None] * self._capacity
        for i in range(self._size):
            self._heap[i] = tmp[i]

    def push(self, val: K) -> None:
        """入堆

        Args:
            val (K): 待入堆元素
        """
        if self._size >= self._capacity: # 扩容
            self._extend()
        self._heap[self._size] = val
        self._sift_up(idx=self._size) # 将尾部追加的节点上浮至合适位置
        self._size += 1

    def pop(self) -> K:
        """出堆

        Raises:
            IndexError: 空堆

        Returns:
            K: 出堆元素
        """
        if self._size == 0:
            raise IndexError("堆为空")
        result: K = self._heap[0] # type: ignore
        self._heap[0] = self._heap[self._size - 1]
        self._heap[self._size - 1] = None
        self._size -= 1 # 因为下沉节点时需要引用堆的长度，务必先更新堆的长度再下沉节点
        self._sift_down(idx=0) # 将交换后新的根节点下沉至合适位置
        return result
    
    def peek(self) -> K:
        """查看堆顶元素

        Raises:
            IndexError: 空堆

        Returns:
            K: 堆顶元素
        """
        if self._size == 0:
            raise IndexError("堆为空")
        return self._heap[0] # type: ignore
    
    def _sift_up(self, idx: int) -> None:
        """上浮节点

        Args:
            idx (int): 待上浮节点
        """
        while idx > 0: # 根节点无需再上浮
            parent: int = (idx - 1) // 2 # 父节点的索引
            if self._heap[parent] >= self._heap[idx]: # type: ignore # 无需再修复节点
                break
            self._heap[parent], self._heap[idx] = self._heap[idx], self._heap[parent] # 修复节点
            idx = parent

    def _sift_down(self, idx: int) -> None:
        """下沉节点

        Args:
            idx (int): 待下沉节点
        """
        while True:
            left: int = 2 * idx + 1 # 左子节点的索引
            if left < self._size: # 存在子节点（叶子节点无需再下沉）
                maximum: int = idx # 记录当前节点和其子节点中的最大节点
                if self._heap[left] > self._heap[idx]: # type: ignore
                    maximum = left
                right: int = 2 * idx + 2 # 右子节点的索引
                if (right < self._size) and (self._heap[right] > self._heap[maximum]): # type: ignore
                    maximum = right
                if maximum != idx: # 需要修复节点
                    self._heap[idx], self._heap[maximum] = self._heap[maximum], self._heap[idx]
                    idx = maximum
                    continue
            break # 无需修复节点

    def __len__(self) -> int:
        """查看堆中元素数量

        Returns:
            int: 堆中元素数量
        """
        return self._size



class MinHeap(MaxHeap[K]): # 只需覆写 MaxHeap 的 _sift_up 方法和 _sift_down 方法即可
    """小顶堆（完全二叉树，任意非叶子节点的值小于等于其子节点的值）"""
    @override
    def _sift_up(self, idx: int) -> None:
        """上浮节点

        Args:
            idx (int): 待上浮节点
        """
        while idx > 0: # 根节点无需再上浮
            parent: int = (idx - 1) // 2 # 父节点的索引
            if self._heap[parent] <= self._heap[idx]: # type: ignore # 无需再修复节点
                break
            self._heap[parent], self._heap[idx] = self._heap[idx], self._heap[parent] # 修复节点
            idx = parent

    @override
    def _sift_down(self, idx: int) -> None:
        """下沉节点

        Args:
            idx (int): 待下沉节点
        """
        while True:
            left: int = 2 * idx + 1 # 左子节点的索引
            if left < self._size: # 存在子节点（叶子节点无需再下沉）
                minimum: int = idx # 记录当前节点和其子节点中的最小节点
                if self._heap[left] < self._heap[idx]: # type: ignore
                    minimum = left
                right: int = 2 * idx + 2 # 右子节点的索引
                if (right < self._size) and (self._heap[right] < self._heap[minimum]): # type: ignore
                    minimum = right
                if minimum != idx: # 需要修复节点
                    self._heap[idx], self._heap[minimum] = self._heap[minimum], self._heap[idx]
                    idx = minimum
                    continue
            break # 无需修复节点



# 优先级队列
class Pair(Generic[K, V]):
    """键值对"""
    def __init__(self, obj: K, attr: V) -> None:
        """构造方法

        Args:
            obj (K): 对象
            attr (V): 与对象绑定的属性
        """
        self.obj: K = obj
        self.attr: V = attr # 用于进行比较的属性


class MaxPriorityQueue(Generic[K, V]):
    """基于大顶堆的优先级队列"""
    extend_ratio: Final[int] = 2 # 每次扩容的倍数（不可变）

    def __init__(self, data: Optional[Sequence[Pair[K, V]]] = None) -> None:
        """构造方法

        Args:
            data (Optional[Sequence[Pair[K, V]]], optional): 待堆化的序列. Defaults to None.
        """
        self._heap: List[Optional[Pair[K, V]]]
        self._capacity: int # 容量
        self._size: int
        if data is None: # 初始化一个空堆
            self._capacity = 10
            self._heap = [None] * self._capacity
            self._size = 0
        else: # 堆化现有数组（非原地）
            self._capacity = len(data)
            self._heap = [None] * self._capacity
            self._size = self._capacity
            last_not_leaf: int = (self._size - 2) // 2 # 最后一个非叶子节点（有可能等于-1）
            for i in range(last_not_leaf + 1, self._size):
                self._heap[i] = data[i]
            for i in range(last_not_leaf, -1, -1):
                # 倒序遍历数组（层序遍历的倒序），依次对每个非叶节点执行“从顶至底堆化”；
                # 每当堆化一个节点后，以该节点为根节点的子树就形成一个合法的子堆。
                self._heap[i] = data[i]
                self._sift_down(idx=i)

    def _extend(self) -> None:
        """扩容"""
        tmp: List[Pair[K, V]] = self._heap # type: ignore
        self._capacity *= self.extend_ratio
        self._heap = [None] * self._capacity
        for i in range(self._size):
            self._heap[i] = tmp[i]

    def enqueue(self, item: Pair[K, V]) -> None:
        """入队

        Args:
            item (Pair[K, V]): 待入队元素_
        """
        if self._size >= self._capacity: # 扩容
            self._extend()
        self._heap[self._size] = item
        self._sift_up(idx=self._size) # 将尾部追加的节点上浮至合适位置
        self._size += 1

    def dequeue(self) -> Pair[K, V]:
        """出队

        Raises:
            IndexError: 空队

        Returns:
            Pair[K, V]: 出队元素
        """
        if self._size == 0:
            raise IndexError("优先级队列为空")
        result: Pair[K, V] = self._heap[0] # type: ignore
        self._heap[0] = self._heap[self._size - 1]
        self._heap[self._size - 1] = None
        self._size -= 1 # 因为下沉节点时需要引用堆的长度，务必先更新堆的长度再下沉节点
        self._sift_down(idx=0) # 将交换后新的根节点下沉至合适位置
        return result
    
    def peek(self) -> Pair[K, V]:
        """查看队首元素

        Raises:
            IndexError: 空队

        Returns:
            Pair[K, V]: 队首元素
        """
        if self._size == 0:
            raise IndexError("优先级队列为空")
        return self._heap[0] # type: ignore
    
    def _sift_up(self, idx: int) -> None:
        """上浮节点

        Args:
            idx (int): 待上浮节点
        """
        while idx > 0: # 根节点无需再上浮
            parent: int = (idx - 1) // 2 # 父节点的索引
            if self._heap[parent].attr >= self._heap[idx].attr: # type: ignore # 无需再修复节点
                break
            self._heap[parent], self._heap[idx] = self._heap[idx], self._heap[parent] # 修复节点
            idx = parent

    def _sift_down(self, idx: int) -> None:
        """下沉节点

        Args:
            idx (int): 待下沉节点
        """
        while True:
            left: int = 2 * idx + 1 # 左子节点的索引
            if left < self._size: # 存在子节点（叶子节点无需再下沉）
                maximum: int = idx # 记录当前节点和其子节点中的最大节点
                if self._heap[left].attr > self._heap[idx].attr: # type: ignore
                    maximum = left
                right: int = 2 * idx + 2 # 右子节点的索引
                if (right < self._size) and (self._heap[right].attr > self._heap[maximum].attr): # type: ignore
                    maximum = right
                if maximum != idx: # 需要修复节点
                    self._heap[idx], self._heap[maximum] = self._heap[maximum], self._heap[idx]
                    idx = maximum
                    continue
            break # 无需修复节点

    def __len__(self) -> int:
        """查看队列长度

        Returns:
            int: 队列长度
        """
        return self._size



class MinPriorityQueue(MaxPriorityQueue[K, V]):
    """基于小顶堆的优先级队列"""
    @override
    def _sift_up(self, idx: int) -> None:
        """上浮节点

        Args:
            idx (int): 待上浮节点
        """
        while idx > 0: # 根节点无需再上浮
            parent: int = (idx - 1) // 2 # 父节点的索引
            if self._heap[parent].attr <= self._heap[idx].attr: # type: ignore # 无需再修复节点
                break
            self._heap[parent], self._heap[idx] = self._heap[idx], self._heap[parent] # 修复节点
            idx = parent

    @override
    def _sift_down(self, idx: int) -> None:
        """下沉节点

        Args:
            idx (int): 待下沉节点
        """
        while True:
            left: int = 2 * idx + 1 # 左子节点的索引
            if left < self._size: # 存在子节点（叶子节点无需再下沉）
                minimum: int = idx # 记录当前节点和其子节点中的最小节点
                if self._heap[left].attr < self._heap[idx].attr: # type: ignore
                    minimum = left
                right: int = 2 * idx + 2 # 右子节点的索引
                if (right < self._size) and (self._heap[right].attr < self._heap[minimum].attr): # type: ignore
                    minimum = right
                if minimum != idx: # 需要修复节点
                    self._heap[idx], self._heap[minimum] = self._heap[minimum], self._heap[idx]
                    idx = minimum
                    continue
            break # 无需修复节点




if __name__ == "__main__":
    data: List[int] = [9, 8, 6, 6, 7, 5, 2, 1, 4, 3, 6, 2]
    h: MinHeap[int] = MinHeap[int](data=data)
    print(h._heap)
    for _ in range(len(data)):
        print(h.pop())
    h2: MaxHeap[int] = MaxHeap[int]()
    for i in range(15):
        h2.push(val=i)
    print(h2._heap)
    print(data)
    m: MinPriorityQueue[str, int] = MinPriorityQueue[str, int]()
    for i in data:
        m.enqueue(item=Pair(obj=str(object=i), attr=i))
    print("大小为", len(m))
    print([i.obj for i in m._heap if i is not None])
    print([i.attr for i in m._heap if i is not None])
    i: int = 0
    for _ in range(len(data)):
        i += 1
        tmp: Pair[str, int] = m.dequeue()
        print(f"第{i}个出队", tmp.obj, tmp.attr)
    l: List[Pair[str, int]] = [Pair(obj=str(object=i), attr=i) for i in range(15)]
    h3 = MinPriorityQueue(data=l)
    print("-------------")
    for _ in range(len(h3)):
        tmp = h3.dequeue()
        print(tmp.obj, tmp.attr)