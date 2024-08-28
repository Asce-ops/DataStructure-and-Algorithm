class TreeNode:
    '''二叉树节点'''
    def __init__(self, key: int, val: str) -> None:
        self.key: int = key # 节点键
        self.val: int = val # 节点值
        self.left: TreeNode | None = None # 左子节点引用
        self.right: TreeNode | None = None # 右子节点引用

class BinarySearchTree:
    '''二叉搜索树（不允许存储重复的元素）'''
    def __init__(self) -> None:
        '''初始化一棵空树'''
        self._root: TreeNode | None = None
        self._size: int = 0

    def put(self, key: int, val: str) -> None:
        '''添加（或修改）元素'''
        if self._root is None: # 空树，直接在根节点存储新元素
            self._root = TreeNode(key=key, val=val)
            self._size += 1
            return
        cur: TreeNode | None = self._root
        while cur is not None: # 新元素只能作为叶子节点插入
            if key < cur.key:
                prev = cur
                cur = cur.left
            elif key > cur.key:
                prev = cur
                cur = cur.right
            else: # 更新元素
                cur.val = val
                return
        node = TreeNode(key=key, val=val)
        if key < prev.key:
            prev.left = node
        else: # 不可能出现 key == prev.key 的情况
            prev.right = node
        self._size += 1

    def remove(self, key: int) -> None:
        '''删除元素'''
        cur: TreeNode | None = self._root # 待删除节点
        prev: TreeNode | None = None # 待删除节点的父节点
        while cur is not None:
            if key < cur.key:
                prev = cur
                cur = cur.left
            elif key > cur.key:
                prev = cur
                cur = cur.right
            else: # 定位到了待删除元素的位置
                '''寻找用于替换待删除节点的元素'''
                if (cur.left is None) or (cur.right is None): # 至多只有一个子节点，用待删除节点唯一的子节点或 None 来替换待删除节点
                    tmp: TreeNode | None = cur.left or cur.right
                else: # 待删除节点同时存在左右子节点，用待删除节点的后继节点（比当前节点大的最小的节点）来替换待删除节点
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
        raise KeyError(f'{key}在二叉搜索树中不存在')
    
    def search(self, key: int) -> str:
        '''查找元素'''
        cur: TreeNode | None = self._root
        while cur is not None:
            if key < cur.key:
                cur = cur.left
            elif key > cur.key:
                cur = cur.right
            else:
                return cur.val
        raise KeyError(f'{key}在二叉搜索树中不存在')
    
    def get_root(self) -> TreeNode | None:
        '''返回根节点'''
        return self._root
    
    def __getitem__(self, key: int) -> str:
        return self.search(key=key)
    
    def __setitem__(self, key: int, val: str) -> None:
        self.put(key=key, val=val)

    def __delitem__(self, key: int) -> None:
        self.remove(key=key)
    
    def __contains__(self, key: int) -> bool:
        try:
            self.search(key=key)
            return True
        except KeyError:
            return False
        
    def __len__(self) -> int:
        return self._size
    


class AvlTreeNode():
    '''AVL树的节点'''
    def __init__(self, key: int, val: str) -> None:
        self.key: int = key # 节点键
        self.val: int = val # 节点值
        self.left: AvlTreeNode | None = None # 左子节点引用
        self.right: AvlTreeNode | None = None # 右子节点引用
        self.parent: AvlTreeNode | None = None # 父节点的引用
        self.height: int = 0 # 规定叶子节点高度为 0
        self.balance_factor: int = 0 # 平衡因子

    def is_left_child(self) -> bool:
        '''判断是否是左子节点'''
        return (self.parent is not None) and (self.parent.left is self)
    
    def is_right_child(self) -> bool:
        '''判断是否是右子节点'''
        return (self.parent is not None) and (self.parent.right is self)
    

class AvlTree():
    '''AVL树'''
    def __init__(self) -> None:
        '''初始化一棵空树'''
        self._root: AvlTreeNode | None = None
        self._size: int = 0

    @staticmethod # 静态方法
    def get_height(node: AvlTreeNode | None) -> int: # 因为需要计算空节点 None 的高度，所以不方便在 AvlTreeNode 类中定义
        '''返回节点的高度（空节点高度为 -1 ，叶子节点高度为 0）'''
        if node is not None:
            return node.height
        return -1
    
    @staticmethod # 静态方法
    def update_height(node: AvlTreeNode) -> None:
        '''更新节点的高度'''
        node.height = max(AvlTree.get_height(node=node.left), AvlTree.get_height(node=node.right)) + 1 # 节点高度等于最高子树高度 + 1
    
    @staticmethod # 静态方法
    def update_balance_factor(node: AvlTreeNode) -> None:
        '''更新节点的平衡因子'''
        node.balance_factor = AvlTree.get_height(node=node.left) - AvlTree.get_height(node=node.right)

    def left_rotate(self, node: AvlTreeNode) -> AvlTreeNode:
        '''
        左旋：
        将右子节点提升为子树的根节点；
        将旧根节点作为新根节点的左子节点；
        如果新根节点已经有一个左子节点，将其作为新左子节点（旧根节点）的右子节点。
        '''
        new_root = node.right # 子树新的根节点
        new_root.parent = node.parent
        if node.parent is None: # 失衡节点是根节点
            self._root = new_root
        elif node.is_left_child(): # 失衡节点是左子节点
            node.parent.left = new_root
        else: # 失衡节点是右子节点
            node.parent.right = new_root
        node.right = new_root.left
        if node.right is not None:
            node.right.parent = node
        new_root.left = node
        node.parent = new_root
        '''更新被调整过的节点的高度和平衡因子'''
        AvlTree.update_height(node=node)
        AvlTree.update_balance_factor(node=node)
        AvlTree.update_height(node=new_root)
        AvlTree.update_balance_factor(node=new_root)
        return new_root

    def right_rotate(self, node: AvlTreeNode) -> AvlTreeNode:
        '''
        右旋：
        将左子节点提升为子树的根节点；
        将旧根节点作为新根节点的右子节点；
        如果新根节点已经有一个右子节点，将其作为新右子节点（旧根节点）的左子节点。
        '''
        new_root = node.left # 子树新的根节点
        new_root.parent = node.parent
        if node.parent is None: # 失衡节点是根节点
            self._root = new_root
        elif node.is_right_child(): # 失衡节点是右子节点
            node.parent.right = new_root
        else: # 失衡节点是左子节点
            node.parent.left = new_root
        node.left = new_root.right
        if node.left is not None:
            node.left.parent = node
        new_root.right = node
        node.parent = new_root
        '''更新被调整过的节点的高度和平衡因子'''
        AvlTree.update_height(node=node)
        AvlTree.update_balance_factor(node=node)
        AvlTree.update_height(node=new_root)
        AvlTree.update_balance_factor(node=new_root)
        return new_root

    def rebalance(self, node: AvlTreeNode) -> AvlTreeNode:
        '''再平衡'''
        if node.balance_factor > 1:
            if node.left.balance_factor < 0: # 先围绕失衡节点的左子节点左旋，再围绕失衡节点右旋
                self.left_rotate(node=node.left)
                new_root = self.right_rotate(node=node)
            else: # 围绕失衡节点右旋
                new_root = self.right_rotate(node=node)
        elif node.balance_factor < -1:
            if node.right.balance_factor > 0: # 先围绕失衡节点的右子节点右旋，再围绕失衡节点左旋
                self.right_rotate(node=node.right)
                new_root = self.left_rotate(node=node)
            else: # 围绕失衡节点左旋
                new_root = self.left_rotate(node=node)
        return new_root

    def put(self, key: int, val: str) -> None:
        '''添加（或修改元素）'''
        if self._root is None: # 空树，直接在根节点存储新元素
            self._root = AvlTreeNode(key=key, val=val)
            self._size += 1
            return
        cur: AvlTreeNode | None = self._root
        while cur is not None: # 新元素只能作为叶子节点插入
            if key < cur.key:
                prev = cur
                cur = cur.left
            elif key > cur.key:
                prev = cur
                cur = cur.right
            else: # 更新元素
                cur.val = val
                return
        node = AvlTreeNode(key=key, val=val)
        if key < prev.key:
            prev.left = node
        else: # 不可能出现 key == prev.key 的情况
            prev.right = node
        node.parent = prev
        self._size += 1
        '''检查新插入节点的各个祖先节点是否失衡'''
        grand: AvlTreeNode | None = prev
        while grand is not None: # 叶子节点的高度和平衡因子无需更新
            AvlTree.update_height(node=grand)
            AvlTree.update_balance_factor(node=grand)
            if (grand.balance_factor > 1) or (grand.balance_factor < -1): # 离新插入节点最近的失衡节点
                self.rebalance(node=grand)
                break # 插入导致的失衡只需要调整一次
            grand = grand.parent

    def successor(self, node: AvlTreeNode) -> AvlTreeNode | None:
        '''寻找给定节点的后继节点'''
        result: AvlTreeNode | None = node.right # 后继节点
        if result is not None:
            while result.left is not None:
                result = result.left
        return result
    
    def remove(self, key: int) -> None:
        '''删除元素'''
        cur: AvlTreeNode | None = self._root # 待删除节点
        while cur is not None:
            if key < cur.key:
                cur = cur.left
            elif key > cur.key:
                cur = cur.right
            else: # 定位到了待删除元素的位置
                '''寻找用于替换待删除节点的元素'''
                if (cur.left is None) or (cur.right is None): # 至多只有一个子节点，用待删除节点唯一的子节点或 None 来替换待删除节点
                    tmp: AvlTreeNode | None = cur.left or cur.right
                    grand: AvlTreeNode | None = cur.parent # 实际被删除节点的父节点
                else: # 待删除节点同时存在左右子节点，用待删除节点的后继节点（比当前节点大的最小的节点）来替换待删除节点
                    tmp: AvlTreeNode | None = self.successor(node=cur) # 后继节点
                    grand: AvlTreeNode | None = tmp.parent # 实际被删除节点的父节点
                    '''删除后继节点'''
                    if tmp.is_left_child(): # 后继节点是其父节点的左子节点
                        tmp.parent.left = tmp.right
                    else: # 后继节点是其父节点的右子节点
                        tmp.parent.right = tmp.right
                    if tmp.right is not None: # 后继节点只可能有右子节点
                        tmp.right.parent = tmp.parent
                    '''用后继节点替换待删除节点（接替子节点关系）'''
                    tmp.left = cur.left
                    cur.left.parent = tmp
                    tmp.right = cur.right
                    cur.right.parent = tmp
                '''用后继节点替换待删除节点（接替父节点关系）'''
                if cur.parent is None: # 待删除的是根节点
                    self._root = tmp
                else:
                    if cur.is_left_child(): # 待删除节点是其父节点的左子节点
                        cur.parent.left = tmp
                    else: # 待删除节点是其父节点的左子节点
                        cur.parent.right = tmp
                    if tmp is not None: # 待删除节点是叶子结点时 tmp 为 None
                        tmp.parent = cur.parent
                self._size -= 1
                cur.parent = cur.left = cur.right = None # 便于内存回收
                '''检查实际被删除节点的各个祖先节点是否失衡'''
                while grand is not None:
                    AvlTree.update_height(node=grand)
                    AvlTree.update_balance_factor(node=grand)
                    if (grand.balance_factor > 1) or (grand.balance_factor < -1): # 离新插入节点最近的失衡节点
                        new_root = self.rebalance(node=grand)
                        grand = new_root.parent
                        continue # 删除导致的失衡可能要调整多次
                    grand = grand.parent
                return
        raise KeyError(f'{key}在AVL树中不存在')

    def search(self, key: int) -> str:
        '''查找元素'''
        cur: AvlTreeNode | None = self._root
        while cur is not None:
            if key < cur.key:
                cur = cur.left
            elif key > cur.key:
                cur = cur.right
            else:
                return cur.val
        raise KeyError(f'{key}在AVL树中不存在')
    
    def get_root(self) -> TreeNode | None:
        '''返回根节点'''
        return self._root
    
    def __getitem__(self, key: int) -> str:
        return self.search(key=key)
    
    def __setitem__(self, key: int, val: str) -> None:
        self.put(key=key, val=val)

    def __delitem__(self, key: int) -> None:
        self.remove(key=key)
    
    def __contains__(self, key: int) -> bool:
        try:
            self.search(key=key)
            return True
        except KeyError:
            return False
        
    def __len__(self) -> int:
        return self._size


'''二叉树的遍历'''
from Queue import ArrayQueue
from LinkedList import LinkedList

def level_order(root: TreeNode | AvlTreeNode | None) -> LinkedList:
    '''层序遍历（即广度优先遍历，从顶部到底部逐层遍历二叉树）'''
    queue: ArrayQueue[TreeNode | AvlTreeNode] = ArrayQueue()
    result: LinkedList = LinkedList()
    if root is not None:
        queue.enqueue(item=root)
    while not queue.is_empty():
        cur: TreeNode = queue.dequeue()
        result.append(val=cur.val)
        if cur.left is not None:
            queue.enqueue(item=cur.left)
        if cur.right is not None:
            queue.enqueue(item=cur.right)
    return result

'''
前序、中序和后序遍历都属于深度优先遍历
前中后指的是每一层的“根节点”；遍历一定是先左后右的，所以前中后序分别是：中左右、左中右、左右中
'''
def pre_order(root: TreeNode | AvlTreeNode | None, result: LinkedList) -> None: # 如果给 result 设置默认值，由于它是可变的数据类型，每一次调用该函数都会使得默认值发生变化，导致除第一次调用外每次调用返回结果都有误
    '''前序遍历，将树中的元素依次追加到 result 中'''
    if root is None:
        return
    '''访问优先级：根节点 -> 左子树 -> 右子树'''
    result.append(val=root.val)
    pre_order(root=root.left, result=result)
    pre_order(root=root.right, result=result)

def in_order(root: TreeNode | AvlTreeNode | None, result: LinkedList) -> None:
    '''中序遍历，将树中的元素依次追加到 result 中'''
    if root is None:
        return
    '''访问优先级：左子树 -> 根节点 -> 右子树'''
    in_order(root=root.left, result=result)
    result.append(val=root.val)
    in_order(root=root.right, result=result)

def post_order(root: TreeNode | AvlTreeNode | None, result: LinkedList) -> None:
    '''后序遍历，将树中的元素依次追加到 result 中'''
    if root is None:
        return
    '''访问优先级：左子树 -> 右子树 -> 根节点'''
    post_order(root=root.left, result=result)
    post_order(root=root.right, result=result)
    result.append(val=root.val)



if __name__ == '__main__':
    myTree = BinarySearchTree()
    for i in [9, 5, 17, 3, 7, 15, 20, 1, 4, 6, 8, 10, 16, 18, 22]:
        myTree.put(key=i, val=str(i))
    print(level_order(root=myTree.get_root()).to_list())
    l1, l2, l3 = LinkedList(), LinkedList(), LinkedList()
    pre_order(root=myTree.get_root(), result=l1)
    print(l1.to_list())
    in_order(root=myTree.get_root(), result=l2)
    print(l2.to_list())
    post_order(root=myTree.get_root(), result=l3)
    print(l3.to_list())


    avl = AvlTree()
    d = [14, 9, 5, 17, 11, 12, 7, 19, 16, 27, 8, 18, 23]
    for i in d:
        avl.put(key=i, val=str(i))
    print(level_order(root=avl.get_root()).to_list())
    avl.remove(key=5)
    print(level_order(root=avl.get_root()).to_list())
    l = LinkedList()
    pre_order(root=avl.get_root(), result=l)
    print(l.to_list())