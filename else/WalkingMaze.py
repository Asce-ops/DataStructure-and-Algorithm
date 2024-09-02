# type: ignore

import sys
from random import shuffle
from pathlib import Path
from copy import deepcopy

sys.path.append(str(Path(__file__).parent.parent)) # Path(__file__) 获取的当前 py 文件的路径

from Stack import ArrayStack
from Queue import ArrayQueue
from Array import DynamicArray
from LinkedList import LinkedList


'''初始化一个迷宫'''
maze = [ # 0 表示不可走，1 表示可走，2 表示出口
    [1, 0, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 2]
]



def DfsMazePath(maze: list[list[0 | 1 | 2]], start: tuple[int, int]) -> list[tuple[int, int]]:
	'''深度优先搜索走迷宫'''
	if maze[start[0]][start[1]] == 2:
		print('起点即出口')
		return
	maze = deepcopy(maze) # 避免修改原迷宫（由于是嵌套列表，需要做深复制）
	m: int = len(maze)
	n: int = len(maze[0])
	stack_path: ArrayStack[tuple[int, int]] = ArrayStack() # 用栈来存放行走路径
	maze[start[0]][start[1]] = -1 # 将入栈的坐标标记为走过
	stack_path.push(item=start)
	directions: list[function] = [ # 当前位置向四个方向移动后的坐标
        lambda x, y: (x + 1, y), # 向下
        lambda x, y: (x - 1, y), # 向上
        lambda x, y: (x, y + 1), # 向右
        lambda x, y: (x, y - 1), # 向左
    ]
	random_directions: list[int] = list(range(4))
	while not stack_path.is_empty():
		cur: tuple[int, int] = stack_path.peek() # 当前位置
		'''寻找可行的下一步'''
		shuffle(x=random_directions) # 原地随机重排
		for i in random_directions:
			next_step: tuple[int, int] = directions[i](x=cur[0], y=cur[1])
			if (0 <= next_step[0] < m) and (0 <= next_step[1] < n): # 没有超出迷宫范围
				if maze[next_step[0]][next_step[1]] == 1: # 可行
					maze[next_step[0]][next_step[1]] = -1 # 将入栈的坐标标记为走过
					stack_path.push(item=next_step)
					break # 找到一个可行的下一步即可
				elif maze[next_step[0]][next_step[1]] == 2: # 找到出口
					stack_path.push(item=next_step)
					return stack_path.to_list()
		else:
			stack_path.pop() # 当前坐标陷入死胡同，退回上一步
	print('从当前起点触发找不到迷宫的出口')



def BfsMazePath(maze: list[list[0 | 1 | 2]], start: tuple[int, int]) -> list[tuple[int, int]]:
	'''广度优先搜索走迷宫'''
	if maze[start[0]][start[1]] == 2:
		print('起点即出口')
		return
	maze = deepcopy(maze) # 避免修改原迷宫（由于是嵌套列表，需要做深复制）
	m: int = len(maze)
	n: int = len(maze[0])
	'''queue 和 path 中额外维护了行走路径中每个坐标的上一个坐标在 path 中的索引'''
	queue: ArrayQueue[tuple[int, int], int] = ArrayQueue() # 行走的路径
	path: DynamicArray[tuple[int, int], int] = DynamicArray() # 避免出队的元素丢失
	maze[start[0]][start[1]] = -1 # 将入队的坐标标记为走过
	queue.enqueue(item=(start, len(path) - 1))
	directions: list[function] = [ # 当前位置向四个方向移动后的坐标
        lambda x, y: (x + 1, y), # 向下
        lambda x, y: (x - 1, y), # 向上
        lambda x, y: (x, y + 1), # 向右
        lambda x, y: (x, y - 1), # 向左
    ]
	while not queue.is_empty():
		cur: tuple[int, int] = queue.dequeue() # 当前位置
		path.append(item=cur)
		cur = cur[0]
		for dir in directions:
			next_step: tuple[int, int] = dir(x=cur[0], y=cur[1])
			if (0 <= next_step[0] < m) and (0 <= next_step[1] < n): # 没有超出迷宫范围
				if maze[next_step[0]][next_step[1]] == 1: # 可行
					maze[next_step[0]][next_step[1]] = -1 # 将入队的坐标标记为走过
					queue.enqueue(item=(next_step, len(path) - 1)) # len(path) - 1 是新出队元素在 path 中的索引
				elif maze[next_step[0]][next_step[1]] == 2: # 找到出口
					result: LinkedList = LinkedList() # 使用链表，数组不方便在头部插入元素
					result.insert(idx=0, val=next_step)
					parent: int = len(path) - 1
					'''从 path 中找到起点至出口的路径'''
					while parent != -1:
						prev_step: tuple[tuple[int, int], int] = path[parent]
						result.insert(idx=0, val=prev_step[0])
						parent = prev_step[1]
					return result.to_list()
	print('从当前起点触发找不到迷宫的出口')



if __name__ == '__main__':
	print(DfsMazePath(maze=maze, start=(0, 0)))
	print(BfsMazePath(maze=maze, start=(0, 0)))