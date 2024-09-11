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

def shell_sort(arr: list[int], asc: bool = True) -> None:
    '''
    希尔排序
    1. 将数组分为若干个子组，对每个子组进行插入排序（让数组变得部分有序）
    2. 更新子组的划分，重复步骤 1（子组的个数必须严格单调递减且最终为1）
    '''
    n: int = len(arr)
    k: int = n // 2 # 组数，前 k 个数作为个组的起点，每隔 k 个数将其作为一组
    while k > 1:
        if asc: # 升序排序
            for i in range(k, n): # 所有组中未排序的部分
                '''对各个组进行插入排序'''
                cur_index: int = i
                while cur_index - k >= 0 and arr[cur_index - k] > arr[cur_index]: # cur_index - interval 是组中有序部分的最后一个元素
                    arr[cur_index], arr[cur_index - k] = arr[cur_index - k], arr[cur_index]
                    cur_index -= k
        else: # 降序排序
            for i in range(k, n): # 所有组中未排序的部分
                '''对各个组进行插入排序'''
                cur_index: int = i
                while cur_index - k >= 0 and arr[cur_index - k] < arr[cur_index]: # cur_index - interval 是组中有序部分的最后一个元素
                    arr[cur_index], arr[cur_index - k] = arr[cur_index - k], arr[cur_index]
                    cur_index -= k
        k //= 2
    insertion_sort(arr=arr, asc=asc)



def merge(arr: list[int], left: int, mid: int, right: int, asc: bool) -> None:
    '''归并排序的辅助函数，用于合并有序的左子数组和右子数组'''
    tmp: list[int | None] = [0] * (right - left + 1) # 创建一个临时数组 tmp ，用于存放合并后的结果
    i, j, k = left, mid + 1, 0 # 初始化左子数组、右子数组和临时数组的起始索引
    if asc: # 升序排序
        while (i <= mid) and (j <= right): # 比较左子数组和右子数组中各自最小的元素
            if arr[i] <= arr[j]:
                tmp[k] = arr[i]
                i += 1
            else:
                tmp[k] = arr[j]
                j += 1
            k += 1
    else: # 降序排序
        while (i <= mid) and (j <= right): # 比较左子数组和右子数组中各自最大的元素
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
    '''将临时数组 tmp 中的元素复制回原数组 arr 的对应区间（归并排序是非原地排序）'''
    for k in range(len(tmp)):
        arr[left + k] = tmp[k]

def merge_sort(arr: list[int], left: int, right: int, asc: bool = True) -> None:
    '''
    归并排序
    1. 划分阶段：通过递归不断地将数组从中点处分开，将长数组的排序问题转换为短数组的排序问题；
    2. 合并阶段：当子数组长度为 1 时终止划分，开始合并，持续地将左右两个较短的有序数组合并为一个较长的有序数组，直至结束。
    '''
    if left >= right: # 子数组长度为1，终止递归
        return
    '''划分阶段'''
    mid = (left + right) // 2 # 计算中点
    merge_sort(arr=arr, left=left, right=mid, asc=asc) # 递归左子数组
    merge_sort(arr=arr, left=mid+1, right=right, asc=asc) # 递归右子数组
    '''合并阶段'''
    merge(arr=arr, left=left, mid=mid, right=right, asc=asc)



def partition(arr: list[int], left: int, right: int, asc: bool) -> int:
    '''快速排序的辅助函数（哨兵划分），用于确定基准数应在有序数组中的位置'''
    pivot: int = arr[left] # 基准数，此时将索引 left 视为一个空的坑
    if asc: # 升序排序
        while left < right:
            '''right 从右往左找比基准数小的元素填 left 的坑'''
            while arr[right] >= pivot: # 因为是以最左边元素作为基准数，所以要先从 right 开始查找
                if left >= right:
                    break
                right -= 1
            else: # 此时将索引 right 视为一个空的坑
                arr[left] = arr[right]
                left += 1 # 避免 left 移动时做一轮无效的比较
            '''left 从左往右找比基准数大的元素填 right 的坑'''
            while arr[left] <= pivot:
                if left >= right:
                    break
                left += 1
            else: # 此时将索引 right 视为一个空的坑
                arr[right] = arr[left]
                right -= 1 # 避免 right 移动时做一轮无效的比较
    else: # 降序排序
        while left < right:
            '''right 从右往左找比基准数大的元素填 left 的坑'''
            while arr[right] <= pivot: # 因为是以最左边元素作为基准数，所以要先从 right 开始查找
                if left >= right:
                    break
                right -= 1
            else: # 此时将索引 right 视为一个空的坑
                arr[left] = arr[right]
                left += 1 # 避免 left 移动时做一轮无效的比较
            '''left 从左往右找比基准数小的元素填 right 的坑'''
            while arr[left] >= pivot:
                if left >= right:
                    break
                left += 1
            else: # 此时将索引 right 视为一个空的坑
                arr[right] = arr[left]
                right -= 1 # 避免 right 移动时做一轮无效的比较
    '''确定了基准数应在有序数组中的位置'''
    arr[left] = pivot # 此时 left == right
    return left

def quick_sort(arr :list[int], left: int, right: int, asc: bool = True) -> None:
    '''
    快速排序
    1. 首先，对原数组执行一次“哨兵划分”，得到未排序的左子数组和右子数组；
    2. 然后，对左子数组和右子数组分别递归执行“哨兵划分”；
    3. 持续递归，直至子数组长度为 1 时终止，从而完成整个数组的排序。
    '''
    if left >= right: # 空数组或只有一个元素的数组
        return
    idx: int = partition(arr=arr, left=left, right=right, asc=asc)
    quick_sort(arr=arr, left=left, right=idx-1, asc=asc) # 递归左子数组
    quick_sort(arr=arr, left=idx+1, right=right, asc=asc) # 递归右子数组



def heap_sort(arr: list[int], asc: bool = True) -> None:
    '''
    堆排序
    1. 输入数组并建立大/小顶堆（倒序遍历将每个元素下沉至合适位置），完成后，最大/小元素位于堆顶；
    2. 将堆顶元素（第一个元素）与堆底元素（最后一个元素）交换，完成交换后，堆的长度减 1，已排序元素数量加 1；
    3. 将新的堆顶元素重新下沉至合适位置，完成堆化后，堆的性质得到修复；
    4. 循环执行第 2 步和第 3 步，循环 n-1 轮后，即可完成数组排序。
    '''
    N: int = len(arr)
    def sift_down(idx: int, n: int, MaxHeap: bool = asc) -> None:
        '''将索引 i 的元素下沉至合适位置'''
        if MaxHeap:
            while True:
                left = 2 * idx + 1 # 左子节点的索引
                if left < n: # 存在子节点（叶子节点无需再下沉）
                    maximum: int = idx # 记录当前节点和其子节点中的最大节点
                    if arr[left] > arr[idx]:
                        maximum = left
                    right = 2 * idx + 2 # 右子节点的索引
                    if (right < n) and (arr[right] > arr[maximum]):
                        maximum = right
                    if maximum != idx: # 需要修复节点
                        arr[idx], arr[maximum] = arr[maximum], arr[idx]
                        idx = maximum
                        continue
                break # 无需修复节点
        else:
            while True:
                left = 2 * idx + 1 # 左子节点的索引
                if left < n: # 存在子节点（叶子节点无需再下沉）
                    minimum: int = idx # 记录当前节点和其子节点中的最小节点
                    if arr[left] < arr[idx]:
                        minimum = left
                    right = 2 * idx + 2 # 右子节点的索引
                    if (right < n) and (arr[right] < arr[minimum]):
                        minimum = right
                    if minimum != idx: # 需要修复节点
                        arr[idx], arr[minimum] = arr[minimum], arr[idx]
                        idx = minimum
                        continue
                break # 无需修复节点
    last_not_leaf = (N - 2) // 2 # 最后一个非叶子节点（有可能等于-1）
    '''堆化（倒序遍历将每个元素下沉至合适位置）'''
    for i in range(last_not_leaf, -1, -1):
        sift_down(idx=i, n=N)
    for i in range(N - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0] # 交换堆顶与堆的最右叶子结点
        sift_down(idx=0, n=i) # 重新将堆顶下沉至合适位置



def bucket_sort(arr: list[int], k: int = 10, asc: bool = True) -> list[int]:
    '''
    桶排序
    1. 初始化 k 个桶，桶本身互相之间是有序的，将待排序数组中的元素分配到这 k 个桶中；
    2. 对每个桶分别执行排序（这里采用编程语言的内置排序函数）；
    3. 按照桶从小到大的顺序合并结果。
    '''
    maximum: int = arr[0]
    minimum: int = arr[0]
    '''原始数据归一化'''
    for i in range(1, len(arr)):
        if arr[i] > maximum:
            maximum = arr[i]
        if arr[i] < minimum:
            minimum = arr[i]
    buckets: list[list] = [[] for _ in range(k)] # 无法事先预知每个桶中会存放多少元素，需使用动态数组（自定义的 DynamicArray 类没有实现 sort 方法，用列表来代替）
    for num in arr:
        i: int = int(k * (num - minimum) / (maximum - minimum)) # [minimum, maximum] -> [0, 1] -> [0, k] -> range(k+1)
        '''添加进对应桶'''
        if i == k:
            buckets[k - 1].append(num)
        else:
            buckets[i].append(num)
    for bucket in buckets: # 桶内排序
        bucket.sort(reverse=not asc)
    result: int = [None] * len(arr)
    idx: int = 0
    if asc: # 升序
        for i in range(0, k, 1): # 桶间是升序的
            for j in buckets[i]:
                result[idx] = j
                idx += 1
    else: # 降序
        for i in range(k - 1, -1, -1): # 桶间是升序的
            for j in buckets[i]:
                result[idx] = j
                idx += 1
    return result
        


def counting_sort(arr: list[int], asc: bool = True) -> list[int]:
    '''
    计数排序
    1. 遍历待排序数组，找出其中最大元素 maximum 和最小元素 minimum，然后创建一个长度为 maximum - minimum + 1 的计数数组 counter；
    2. 借助计数数组 counter 统计待排序数组中各元素的出现次数，其中 counter[num - minimum] 对应元素 num 的出现次数；
    3. 对计数数组 counter 进行累积计数，即将每个元素的计数值加上前一个元素的计数值，得到每个元素在排序后数组中的位置，这一步确保相同元素的相对顺序不变；
    4. 排序，创建一个与待排序数组大小相同的结果数组，然后遍历待排序数组，根据元素的值在累积计数数组 counter 中找到其在结果数组中的位置，将元素放置在结果数组中的正确位置。
    '''
    maximum: int = arr[0]
    minimum: int = arr[0]
    '''确定计数数组所需的容量'''
    for i in range(1, len(arr)):
        if arr[i] > maximum:
            maximum = arr[i]
        if arr[i] < minimum:
            minimum = arr[i]
    counter: list[int] = [0] * (maximum - minimum + 1)
    for num in arr: # 统计各个元素出现的次数
        counter[num - minimum] += 1
    n: int = len(arr)
    result: list[int | None] = [None] * n
    if asc: # 升序排序
        '''求 counter 的前缀和，将“出现次数”转换为“尾索引”'''
        for i in range(maximum - minimum):
            counter[i + 1] += counter[i]
        '''counter[num - minimum] - 1 是 num 应在有序数组中最后一次出现的索引'''
    else: # 倒序排序
        for i in range(maximum - minimum, 0, -1):
            counter[i - 1] += counter[i]
    for i in range(n - 1, -1, -1): # 倒序遍历以确保相同元素的相对顺序不变
        num = arr[i]
        result[counter[num - minimum] - 1] = num # 将 num 放置到对应索引处
        counter[num - minimum] -= 1 # 令前缀和自减 1，得到下次放置 num 的索引
    return result



def radix_sort(arr: list[int], d: int = 10, asc: bool = True) -> list[int]:
    '''
    基数排序
    1. 初始化位数 k = 1；
    2. 根据待排序数组元素的从右至左第 k 位执行“计数排序”；
    3. 令 k 自增 1 ，然后返回步骤 2. 继续迭代，直到所有位都排序完成后结束。
    '''
    n: int = len(arr)
    def digit(num: int, k: int) -> int:
        '''获取 d 进制数字 num 从右至左的第 k 位'''
        return (num // d**(k-1)) % d
    def counter_sort_digit(arr: list[int], k: int) -> list[int]:
        '''
        计数排序（根据数组每个元素从右至左第 k 位进行排序）
        如果第 k 位相等，则元素的相对位置不变（由第 k-1 位决定）
        '''
        counter: list[int] = [0] * d # d 进制的范围是0~d-1，因此需要容量为 d 的计数数组
        result: list[int | None] = [None] * n
        '''统计 d 进制中各个数字出现的次数'''
        for num in arr:
            x: int = digit(num=num, k=k)
            counter[x] += 1
        if asc: # 升序排序
            '''求 counter 的前缀和，将“出现次数”转换为“尾索引”'''
            for i in range(d - 1):
                counter[i + 1] += counter[i]
        else: # 降序排序
            for i in range(d - 1, 0, -1):
                counter[i - 1] += counter[i]
        for i in range(n - 1, -1, -1): # 倒序遍历以确保相同元素的相对顺序不变
            num = arr[i]
            x: int = digit(num=num, k=k)
            result[counter[x] - 1] = num # 将 num 放置到对应索引处
            counter[x] -= 1 # 令前缀和自减 1，得到下次放置 num 的索引
        return result
    '''确定最大位数'''
    maximum: int = arr[0]
    minimum: int = arr[0]
    for i in range(1, n):
        if arr[i] > maximum:
            maximum = arr[i]
        if arr[i] < minimum:
            minimum = arr[i]
    if minimum < 0: # 存在负整数则将所有元素在相对大小不变的情况下转换为非负整数
        arr: list[int] = arr.copy()
        for i in range(n):
            arr[i] -= minimum
        maximum -= minimum
    exp: int = 1
    k: int = 1
    if maximum == 0: # 说明数组全为 0
        return arr
    result: list[int] = arr
    '''因为高位数比低位数更能决定排序结果，所以从最低位开始排序，让后一轮排序能覆盖前一轮排序的结果'''
    while exp <= maximum:
        result = counter_sort_digit(arr=result, k=k)
        k += 1
        exp *= d
    if minimum < 0: # 还原回原数据
        for i in range(n):
            result[i] += minimum
    return result



if __name__ == '__main__':
    from random import randrange
    from time import time
    start: float = time()
    arr: list[int] = [randrange(start=0, stop=1000) for _ in range(10000)]
    short_bubble_sort(arr=arr, asc=False)
    end: float = time()
    result: list[int] = sorted(arr, reverse=True)
    if result == arr:
        print(f'True，冒泡排序耗时{end - start}')
    else:
        print('False，冒泡排序错误')
    start: float = time()
    arr: list[int] = [randrange(start=0, stop=1000) for _ in range(10000)]
    selection_sort(arr=arr, asc=False)
    end: float = time()
    result: list[int] = sorted(arr, reverse=True)
    if result == arr:
        print(f'True，选择排序耗时{end - start}')
    else:
        print('False，选择排序错误')
    start: float = time()
    arr: list[int] = [randrange(start=0, stop=1000) for _ in range(10000)]
    insertion_sort(arr=arr, asc=False)
    end: float = time()
    result: list[int] = sorted(arr, reverse=True)
    if result == arr:
        print(f'True，插入排序耗时{end - start}')
    else:
        print('False，插入排序错误')
    start: float = time()
    arr: list[int] = [randrange(start=0, stop=1000) for _ in range(10000)]
    shell_sort(arr=arr, asc=False)
    end: float = time()
    result: list[int] = sorted(arr, reverse=True)
    if result == arr:
        print(f'True，希尔排序耗时{end - start}')
    else:
        print('False，希尔排序错误')
    start: float = time()
    arr: list[int] = [randrange(start=0, stop=1000) for _ in range(10000)]
    merge_sort(arr=arr, asc=False, left=0, right=len(arr)-1)
    end: float = time()
    result: list[int] = sorted(arr, reverse=True)
    if result == arr:
        print(f'True，归并排序耗时{end - start}')
    else:
        print('False，归并排序错误')
    start: float = time()
    arr: list[int] = [randrange(start=0, stop=1000) for _ in range(10000)]
    quick_sort(arr=arr, asc=False, left=0, right=len(arr)-1)
    end: float = time()
    result: list[int] = sorted(arr, reverse=True)
    if result == arr:
        print(f'True，快速排序耗时{end - start}')
    else:
        print('False，快速排序错误')
    start: float = time()
    arr: list[int] = [randrange(start=0, stop=1000) for _ in range(10000)]
    heap_sort(arr=arr, asc=False)
    end: float = time()
    result: list[int] = sorted(arr, reverse=True)
    if result == arr:
        print(f'True，堆排序耗时{end - start}')
    else:
        print('False，堆排序错误')
    start: float = time()
    arr: list[int] = [randrange(start=0, stop=1000) for _ in range(10000)]
    result2: list[int] = bucket_sort(arr=arr, asc=False)
    end: float = time()
    result: list[int] = sorted(arr, reverse=True)
    if result == result2:
        print(f'True，桶排序耗时{end - start}')
    else:
        print('False，桶排序错误')
    start: float = time()
    arr: list[int] = [randrange(start=0, stop=1000) for _ in range(10000)]
    result2: list[int] = counting_sort(arr=arr, asc=False)
    end: float = time()
    result: list[int] = sorted(arr, reverse=True)
    if result == result2:
        print(f'True，计数排序耗时{end - start}')
    else:
        print('False，计数排序错误')
    start: float = time()
    arr: list[int] = [randrange(start=0, stop=1000) for _ in range(10000)]
    result2: list[int] = radix_sort(arr=arr, asc=False)
    end: float = time()
    result: list[int] = sorted(arr, reverse=True)
    if result == result2:
        print(f'True，基数排序耗时{end - start}')
    else:
        print('False，基数排序错误')
    start: float = time()
    arr: list[int] = [randrange(start=0, stop=1000) for _ in range(10000)]
    arr.sort(reverse=True)
    end: float = time()
    print(f'True，内置排序耗时{end - start}')