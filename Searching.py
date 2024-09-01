def OrderedSequentialSearch(arr: list[int], item: int, asc: bool = True) -> bool:
    '''有序数组的顺序查找'''
    if asc: # 升序数组
        for i in range(0, len(arr), 1):
            if item > arr[i]:
                continue
            elif item < arr[i]:
                return False
            else: # item == arr[i]
                return True
    else: # 降序
        for i in range(len(arr) - 1, -1, -1):
            if arr[i] < item:
                continue
            elif arr[i] > item:
                return False
            else: # arr[i] == item
                return True



def BinarySearch(arr: list[int], item: int) -> bool:
    '''有序数组的二分查找'''
    first: int = 0
    last: int = len(arr) - 1
    while first <= last:
        middle: int = (first + last) // 2
        if item < arr[middle]:
            last = middle - 1
        elif item > arr[middle]:
            first = middle + 1
        else: # item == arr[middle]
            return True
    return False

def RecursiveBinarySearch(arr: list[int], item: int, first: int, last: int) -> bool:
    '''二分查找的递归版本'''
    if first > last:
        return False
    middle: int = (last + first) // 2
    if item < arr[middle]:
        return RecursiveBinarySearch(arr=arr, item=item, first=first, last=middle-1)
    elif item > arr[middle]:
        return RecursiveBinarySearch(arr=arr, item=item, first=middle+1, last=last)
    else: # item == arr[middle]
        return True



if __name__ == '__main__':
    import Sorting
    arr: list[int] = [49, 99, 92, 121, 31, 96, 132, 145, 169, 0, 158]
    Sorting.quick_sort(arr=arr, left=0, right=len(arr)-1)
    item: int = 9
    print(OrderedSequentialSearch(arr=arr, item=item))
    print(BinarySearch(arr=arr, item=item))
    print(RecursiveBinarySearch(arr=arr, item=item, first=0, last=len(arr)-1))
    item2: int = 96
    print(OrderedSequentialSearch(arr=arr, item=item2))
    print(BinarySearch(arr=arr, item=item2))
    print(RecursiveBinarySearch(arr=arr, item=item2, first=0, last=len(arr)-1))