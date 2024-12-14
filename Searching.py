from typing import List, TypeVar

from utils import Comparable



T = TypeVar(name="T", bound=Comparable)

def OrderedSequentialSearch(arr: List[T], item: T, asc: bool = True) -> bool: # type: ignore
    """有序数组的顺序查找

    Args:
        arr (List[T]): 待查询的有序数组
        item (T): 待查询元素
        asc (bool, optional): 有序数组是否是升序. Defaults to True.

    Returns:
        bool: 待查询元素在有序数组中是否存在
    """
    if asc: # 升序数组
        for i in range(0, len(arr), 1):
            if item > arr[i]:
                continue
            elif item < arr[i]:
                return False
            else: # item == arr[i]
                return True
    else: # 降序数组
        for i in range(len(arr) - 1, -1, -1):
            if arr[i] < item:
                continue
            elif arr[i] > item:
                return False
            else: # arr[i] == item
                return True



def BinarySearch(arr: List[T], item: T, asc: bool = True) -> bool:
    """有序数组的二分查找"""
    first: int = 0
    last: int = len(arr) - 1
    if asc: # 升序数组
        while first <= last:
            middle: int = (first + last) // 2
            if item < arr[middle]:
                last = middle - 1
            elif item > arr[middle]:
                first = middle + 1
            else: # item == arr[middle]
                return True
    else: # 降序数组
        while first <= last:
            middle: int = (first + last) // 2
            if item < arr[middle]:
                first = middle + 1
            elif item > arr[middle]:
                last = middle - 1
            else: # item == arr[middle]
                return True
    return False



def RecursiveBinarySearch(arr: List[T], item: T, first: int, last: int, asc: bool = True) -> bool:
    """二分查找的递归版本"""
    if first > last:
        return False
    middle: int = (last + first) // 2
    if asc: # 升序数组
        if item < arr[middle]:
            return RecursiveBinarySearch(arr=arr, item=item, first=first, last=middle-1, asc=asc)
        elif item > arr[middle]:
            return RecursiveBinarySearch(arr=arr, item=item, first=middle+1, last=last, asc=asc)
        else: # item == arr[middle]
            return True
    else: # 降序数组
        if item > arr[middle]:
            return RecursiveBinarySearch(arr=arr, item=item, first=first, last=middle-1, asc=asc)
        elif item < arr[middle]:
            return RecursiveBinarySearch(arr=arr, item=item, first=middle+1, last=last, asc=asc)
        else: # item == arr[middle]
            return True



if __name__ == "__main__":
    from Sorting import quick_sort
     
    arr: List[int] = [49, 99, 92, 121, 31, 96, 132, 145, 169, 0, 158]
    quick_sort(arr=arr, left=0, right=len(arr)-1, asc=False)
    item: int = 9
    print(OrderedSequentialSearch(arr=arr, item=item, asc=False))
    print(BinarySearch(arr=arr, item=item, asc=False))
    print(RecursiveBinarySearch(arr=arr, item=item, first=0, last=len(arr)-1, asc=False))
    item2: int = 96
    print(OrderedSequentialSearch(arr=arr, item=item2, asc=False))
    print(BinarySearch(arr=arr, item=item2, asc=False))
    print(RecursiveBinarySearch(arr=arr, item=item2, first=0, last=len(arr)-1, asc=False))