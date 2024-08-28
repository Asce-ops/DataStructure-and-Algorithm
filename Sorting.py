def bubble_sort(arr: list[int], asc: bool = True) -> None:
    '''冒泡排序
    1. 首先，对 n 个元素执行“冒泡”，将数组的最大元素交换至正确位置；
    2. 接下来，对剩余 n-1 个元素执行“冒泡”，将第二大元素交换至正确位置；
    3. 以此类推，经过 n-1 轮“冒泡”后，前 n-1 大的元素都被交换至正确位置；
    4. 仅剩的一个元素必定是最小元素，无须排序，因此数组排序完成。
    '''
    n = len(arr)
    if asc: # 升序排序
        for i in range(1, n): # 外循环：未排序区间为 [0, i]
            for j in range(n - i): # 内循环：将未排序区间 [0, i] 中的最大元素交换至该区间的最右端
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
    else: # 降序排序
        for i in range(1, n): # 外循环：未排序区间为 [0, i]
            for j in range(n - i): # 内循环：将未排序区间 [0, i] 中的最小元素交换至该区间的最右端
                if arr[j] < arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]


def short_bubble_sort(arr: list[int], asc: bool = True) -> None:
    '''
    短冒泡排序
    如果某一轮冒泡中没有任何元素交换位置，则元素的顺序已被排好，无需进行后续轮次的冒泡
    '''
    n = len(arr)
    if asc: # 升序排序
        for i in range(1, n): # 外循环：未排序区间为 [0, i]
            order = True
            for j in range(n - i): # 内循环：将未排序区间 [0, i] 中的最大元素交换至该区间的最右端
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    order = False
            if order == True:
                break
    else: # 降序排序
        for i in range(1, n): # 外循环：未排序区间为 [0, i]
            order = True
            for j in range(n - i): # 内循环：将未排序区间 [0, i] 中的最小元素交换至该区间的最右端
                if arr[j] < arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    order = False
            if order == True:
                break



def selection_sort(arr: list[int], asc: bool = True) -> None:
    '''
    选择排序
    1. 初始状态下，所有元素未排序，即未排序（索引）区间为 [0, n-1]；
    2. 选取区间 [0, n-1] 中的最小元素，将其与索引 0 处的元素交换。完成后，数组前 1 个元素已排序；
    3. 选取区间 [1, n-1] 中的最小元素，将其与索引 1 处的元素交换。完成后，数组前 2 个元素已排序；
    4. 以此类推，经过 n-1 轮选择与交换后，数组前 n-1 个元素已排序；
    5. 仅剩的一个元素必定是最大元素，无须排序，因此数组排序完成。
    '''
    n = len(arr)
    if asc: # 升序排序
        for i in range(n - 1): # 外循环：未排序区间为 [i, n-1]
            min_index = i # 记录未排序的最小元素的索引
            for j in range(i + 1, n): # 内循环：找到未排序区间内的最小元素
                if arr[j] < arr[min_index]:
                    min_index = j
            if i != min_index: # 索引 i 不是最小元素时，将索引i的元素和最小元素（min_index 索引的元素）互换位置
                arr[i], arr[min_index] = arr[min_index], arr[i]
    else: # 降序排序
        for i in range(n - 1): # 外循环：未排序区间为 [i, n-1]
            max_index = i # 记录未排序的最大元素的索引
            for j in range(i + 1, n): # 内循环：找到未排序区间内的最大元素
                if arr[j] > arr[max_index]:
                    max_index = j
            if i != max_index: # 索引 i 不是最大元素时，将索引 i 的元素和最大元素（max_index 索引的元素）互换位置
                arr[i], arr[max_index] = arr[max_index], arr[i]



def insertion_sort(arr: list[int], asc: bool = True) -> None:
    '''
    插入排序
    1. 初始状态下，数组的第 1 个元素已完成排序；
    2. 选取数组的第 2 个元素作为 base，将其插入到正确位置后（通过跟已排序区间中的元素进行比较交换位置），数组的前 2 个元素已排序；
    3. 选取第 3 个元素作为 base，将其插入到正确位置后，数组的前 3 个元素已排序；
    4. 以此类推，在最后一轮中，选取最后一个元素作为 base，将其插入到正确位置后，所有元素均已排序。
    '''
    if asc: # 升序排序
        for i in range(1, len(arr)): # 外循环：已排序区间为 [0, i-1]
            base = i
            while (base - 1 >= 0) and (arr[base - 1] > arr[base]): # 内循环：将 arr[base] 插入到已排序区间 [0, i-1] 中的正确位置
                arr[base], arr[base - 1] = arr[base - 1], arr[base]
                base -= 1
    else: # 降序排序
        for i in range(1, len(arr)): # 外循环：已排序区间为 [0, i-1]
            base = i
            while (base - 1 >= 0) and (arr[base - 1] < arr[base]): # 内循环：将 arr[base] 插入到已排序区间 [0, i-1] 中的正确位置
                arr[base], arr[base - 1] = arr[base - 1], arr[base]
                base -= 1


def shell_sort(arr: list[int]) -> None:
    '''
    希尔排序
    '''
    k = 3 # 第一次分组时每组最多包含的元素个数
    n = len(arr)
    interval = int(n / k) # 步长同时也是子列表的个数
    while interval > 0: # 将列表变为“几乎排好序的状态”
        for i in range(interval, n): # 所有子表未排序部分
            cur_index = i
            while cur_index - interval >= 0 and arr[cur_index - interval] > arr[cur_index]:
                arr[cur_index], arr[cur_index - interval] = arr[cur_index - interval], arr[cur_index]
                cur_index -= interval
        interval = int(interval / 3) # int函数会向下取整
    insertion_sort(arr=arr) # 对“几乎排好序”的列表进行插入排序



def merge(arr: list[int], left: int, mid: int, right: int, asc: bool):
    '''并归排序的辅助函数，用于合并有序的左子数组和右子数组'''
    tmp: list[int | None] = [0] * (right - left + 1) # 创建一个临时数组 tmp ，用于存放合并后的结果
    i, j, k = left, mid + 1, 0 # 初始化左子数组、右子数组和临时数组的起始索引
    if asc: # 升序排序
        while (i <= mid) and (j <= right): # 比较左子数组和右子数组中最小的元素
            if arr[i] <= arr[j]:
                tmp[k] = arr[i]
                i += 1
            else:
                tmp[k] = arr[j]
                j += 1
            k += 1
    else: # 降序排序
        while (i <= mid) and (j <= right): # 比较左子数组和右子数组中最大的元素
            if arr[i] >= arr[j]:
                tmp[k] = arr[i]
                i += 1
            else:
                tmp[k] = arr[j]
                j += 1
            k += 1
    '''将左子数组和右子数组的剩余元素复制到临时数组中（左子数组和右子数组有且仅有一个存在剩余元素）'''
    while i <= mid:
        tmp[k] = arr[i]
        i += 1
        k += 1
    while j <= right:
        tmp[k] = arr[j]
        j += 1
        k += 1
    '''将临时数组 tmp 中的元素复制回原数组 arr 的对应区间'''
    for k in range(len(tmp)):
        arr[left + k] = tmp[k]

def merge_sort(arr: list[int], left: int, right: int, asc: bool = True):
    '''
    并归排序
    1. 划分阶段：通过递归不断地将数组从中点处分开，将长数组的排序问题转换为短数组的排序问题；
    2. 合并阶段：当子数组长度为 1 时终止划分，开始合并，持续地将左右两个较短的有序数组合并为一个较长的有序数组，直至结束。
    '''
    if left >= right: # 子数组长度为1，终止递归
        return
    '''划分阶段'''
    mid = (left + right) // 2 # 计算中点
    merge_sort(arr=arr, left=left, right=mid) # 递归左子数组
    merge_sort(arr=arr, left=mid+1, right=right) # 递归右子数组
    '''合并阶段'''
    merge(arr=arr, left=left, right=right, asc=asc)



def 