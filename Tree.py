class TreeNode:
    '''二叉树节点'''
    def __init__(self, val: int) -> None:
        self.val: int = val # 节点值
        self.left: TreeNode | None = None # 左子节点引用
        self.right: TreeNode | None = None # 右子节点引用

class BinarySearchTree:
    '''二叉搜索树（不允许存储重复的元素）'''
    def __init__(self) -> None:
        '''初始化一棵空树'''
        self._root: TreeNode | None = None
        self._size: int = 0

    def put(self, val: int) -> None:
        '''添加元素'''
        node = TreeNode(val=val)
        if self._root is None: # 空树，直接在根节点存储新元素
            self._root = node
            self._size += 1
            return
        cur: TreeNode | None = self._root
        while cur is not None: # 新元素只能作为叶子节点插入
            if val < cur.val:
                prev = cur
                cur = cur.left
            elif val > cur.val:
                prev = cur
                cur = cur.right
            else:
                raise ValueError(f'{val}在二叉搜索树中已存在')
        if val < prev.val:
            prev.left = node
        else: # 不可能出现 val == prev.val 的情况
            prev.right = node
        self._size += 1

    def remove(self, val: int) -> None:
        '''删除元素'''
        cur: TreeNode | None = self._root # 待删除节点
        prev: TreeNode | None = None # 待删除节点的父节点
        while cur is not None:
            if val < cur.val:
                prev = cur
                cur = cur.left
            elif val > cur.val:
                prev = cur
                cur = cur.right
            else: # 定位到了待删除元素的位置
                '''寻找用于替换待删除节点的元素'''
                if (cur.left is None) or (cur.right is None): # 用待删除节点唯一的子节点或 None 来替换待删除节点
                    tmp: TreeNode | None = cur.left or cur.right
                else: # 用待删除节点的后继节点（比当前节点大的最小的节点）来替换待删除节点
                    tmp: TreeNode | None = cur.right # 后继节点
                    tmp_prev: TreeNode = cur # 后继节点的父节点
                    while tmp.left is not None:
                        tmp_prev = tmp
                        tmp = tmp.left
                    '''删除后继节点'''
                    if tmp_prev.left == tmp: # 后继节点是其父节点的左子节点
                        tmp_prev.left = tmp.right
                    else: # 后继节点是其父节点的右子节点
                        tmp_prev.right = tmp.right
                    '''用后继节点替换待删除节点（接替子节点关系）'''
                    tmp.left = cur.left
                    tmp.right = cur.right
                '''用后继节点替换待删除节点（接替父节点关系）'''
                if prev is None: # 待删除的是根节点
                    self._root = tmp
                else:
                    if prev.left == cur: # 待删除节点是其父节点的左子节点
                        prev.left = tmp
                    else: # 待删除节点是其父节点的左子节点
                        prev.right = tmp
                self._size -= 1
                cur.left = cur.right = None # 便于内存回收
                return
        raise ValueError(f'{val}在二叉搜索树中不存在')
    
    def search(self, val: int) -> TreeNode:
        '''查找元素'''
        cur: TreeNode | None = self._root
        while cur is not None:
            if val < cur.val:
                prev = cur
                cur = cur.left
            elif val > cur.val:
                prev = cur
                cur = cur.right
            else:
                return cur
        raise ValueError(f'{val}在二叉搜索树中不存在')
    
    def get_root(self) -> TreeNode | None:
        '''返回根节点'''
        return self._root
    
    def __contains__(self, val: int) -> bool:
        try:
            self.search(val=val)
            return True
        except ValueError:
            return False
        
    def __len__(self) -> int:
        return self._size
    


from Queue import ArrayQueue
from Array import DynamicArray

def level_order(root: TreeNode | None) -> DynamicArray:
    '''层序遍历（即广度优先遍历，从顶部到底部逐层遍历二叉树）'''
    queue: ArrayQueue[TreeNode] = ArrayQueue()
    result: DynamicArray[int] = DynamicArray()
    if root is not None:
        queue.enqueue(item=root)
    while not queue.is_empty():
        cur: TreeNode = queue.dequeue()
        result.append(item=cur.val)
        if cur.left is not None:
            queue.enqueue(item=cur.left)
        if cur.right is not None:
            queue.enqueue(item=cur.right)
    return result

'''
前序、中序和后序遍历都属于深度优先遍历
前中后指的是每一层的“根节点”；遍历一定是先左后右的，所以前中后序分别是：中左右、左中右、左右中
'''
def pre_order(root: TreeNode | None, result: DynamicArray = DynamicArray()) -> DynamicArray:
    '''前序遍历'''
    if root is None:
        return result
    '''访问优先级：根节点 -> 左子树 -> 右子树'''
    result.append(item=root.val)
    result = pre_order(root=root.left, result=result)
    result = pre_order(root=root.right, result=result)
    return result

def in_order(root: TreeNode | None, result: DynamicArray = DynamicArray()) -> DynamicArray:
    '''中序遍历'''
    if root is None:
        return result
    '''访问优先级：左子树 -> 根节点 -> 右子树'''
    result = in_order(root=root.left, result=result)
    result.append(item=root.val)
    result = in_order(root=root.right, result=result)
    return result

def post_order(root: TreeNode | None, result: DynamicArray = DynamicArray()) -> DynamicArray:
    '''后序遍历'''
    if root is None:
        return result
    '''访问优先级：左子树 -> 右子树 -> 根节点'''
    result = post_order(root=root.left, result=result)
    result = post_order(root=root.right, result=result)
    result.append(item=root.val)
    return result



class AvlTreeNode(TreeNode):
    '''AVL树的节点'''
    def __init__(self, val: int) -> None:
        super().__init__(val=val)
        self.height: int = 0 # 节点高度

class AvlTree(BinarySearchTree):
    '''AVL树'''
    def __init__(self) -> None:
        super().__init__()

    @staticmethod # 静态方法
    def get_height(node: AvlTreeNode | None) -> int:
        '''返回节点高度（空节点高度为 -1 ，叶节点高度为 0）'''
        if node is not None:
            return node.height
        return -1
    
    @staticmethod # 静态方法
    def update_height(node: AvlTreeNode | None) -> None:
        if node is not None: # 节点高度等于最高子树高度 + 1
            node.height = max(AvlTree.get_height(node=node.left), AvlTree.get_height(node=node.right)) + 1
    
    @staticmethod
    def get_balance_factor()