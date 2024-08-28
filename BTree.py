# type: ignore
from math import ceil

class BTreeNode():
    '''B树的节点'''
    def __init__(self, capacity: int) -> None:
		self.capacity: int = capacity # 节点的容量
		self.bucket: list[int | None] = [None] * self.capacity # 节点内的有序数组（升序排列）
        self.size: int = 0 # 节点中实际存储的元素个数
		self.child: list[BTreeNode | None] = [None] * (self.capacity + 1) # 分支（分支数是节点中元素个数 +1）
		self.paent: BTreeNode | None = None # 父节点
		self.isleaf: bool = True # 是否是叶子结点
	
	def push(self, val: int) -> None:
		'''在节点中插入元素'''
		if self.size == 0: # 在空节点中插入元素
			self.bucket[0] = val
		cur: int = 0
		while val >= self.bucket[cur]: # 定位到待插入元素的应该放置的位置
			cur += 1
		for i in range(self.size, cur, -1): # 比待插入元素大的元素一次向后挪一个位置
			self.bucket[i] = self.bucket[i-1]
		self.bucket[cur] = val

	def delete(self, val: int) -> None:
		'''在节点中删除元素'''
		

	
class BTree:
	'''B树'''
	def __init__(self, degree: int) -> None:
		'''构建一棵空的B树'''
		self.root: BTreeNode | None = None # 根节点
		self.max_branch: int = degree # 每个节点所有拥有的最大分支数
		self.min_branch: int = ceil(degree / 2) # 根节点外每个节点必须拥有的最小分支数（根节点至少要有 2 个分支，1 个元素）
		self.size: int = 0 # B树中存储的元素个数

	def insert(self, val:int) -> None:
		'''插入节点'''
		if self.root is None:
			self.root = BTreeNode(capacity=self.max_branch-1)
			