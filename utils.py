from abc import ABC, abstractmethod

class Iterator(ABC):
    '''迭代器'''
    @abstractmethod
    def __next__(self) -> object:
        '''返回迭代器的下一个元素'''