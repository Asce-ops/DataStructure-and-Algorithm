from abc import ABC, abstractmethod
from typing import Protocol, Self, TypeVar, runtime_checkable



class Iterator(ABC):
    """定义一个迭代器接口"""
    @abstractmethod
    def __next__(self) -> object:
        """返回迭代器的下一个元素

        Returns:
            object: 
        """
        pass

    def __iter__(self) -> Self:
        """保证迭代器自身是可迭代的

        Returns:
            Self: 自身
        """
        return self
    


T = TypeVar(name="T")

@runtime_checkable # 可使用 isinstance 等函数判断对象是否实现了 Comparable 协议
class Comparable(Protocol):
    """定义一个可比较对象的协议"""
    @abstractmethod
    def __eq__(self: T, value: T, /) -> bool:
        """self: T 使得 T 表示对象自身所属的类"""
        pass

    @abstractmethod
    def __le__(self: T, value: T, /) -> bool:
        pass

    @abstractmethod
    def __ge__(self: T, value: T, /) -> bool:
        pass

    @abstractmethod
    def __lt__(self: T, value: T, /) -> bool:
        pass

    @abstractmethod
    def __gt__(self: T, value: T, /) -> bool:
        pass