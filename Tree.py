from typing import Generic, TypeVar, Optional, List, Tuple, override

from Queue import ArrayQueue
from LinkedList import LinkedList
from utils import Iterator, Comparable



K = TypeVar(name="K", bound=Comparable) # 声明一个类型参数，不宜对其进行 type hints
V = TypeVar(
            name="V", 
            # covariant=True
        )

class TreeNode(Generic[K, V]):
    """二叉树节点"""
    def __init__(self, key: K, val: V) -> None:
        """构造方法

        Args:
            key (K): 键
            val (V): 值
        """
        self.key: K = key # 节点键
        self.val: V = val # 节点值
        self.left: Optional[TreeNode[K, V]] = None # 左子节点引用
        self.right: Optional[TreeNode[K, V]] = None # 右子节点引用

class BinarySearchTree(Generic[K, V]):
    """二叉搜索树（不允许存储重复的元素）"""
    def __init__(self) -> None:
        """构造方法（初始化一棵空的二叉搜索树）"""
        self._root: Optional[TreeNode[K, V]] = None
        self._size: int = 0

    def put(self, key: K, val: V) -> None:
        """新增或更新键值对

        Args:
            key (K): 键
            val (V): 值
        """
        if self._root is None: # 空树，直接在根节点存储新元素
            self._root = TreeNode(key=key, val=val)
            self._size += 1
            return
        cur: Optional[TreeNode[K, V]] = self._root
        prev: TreeNode[K, V] # 用以记录前一个 cur
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
        # 此时prev 必已绑定，否则程序已经结束运行
        node: TreeNode = TreeNode(key=key, val=val)
        if key < prev.key: # type: ignore
            prev.left = node # type: ignore
        else: # 不可能出现 key == prev.key 的情况
            prev.right = node # type: ignore
        self._size += 1

    def remove(self, key: K) -> None:
        """删除键值对

        Args:
            key (K): 待删除的键

        Raises:
            KeyError: 待删除的键在树中不存在
        """
        cur: Optional[TreeNode[K, V]] = self._root # 待删除节点
        prev: Optional[TreeNode[K, V]] = None # 待删除节点的父节点
        while cur is not None:
            if key < cur.key:
                prev = cur
                cur = cur.left
            elif key > cur.key:
                prev = cur
                cur = cur.right
            else: # 定位到了待删除元素的位置
                # 寻找用于替换待删除节点的元素
                tmp: Optional[TreeNode[K, V]] # 后继节点
                if (cur.left is None) or (cur.right is None): # 至多只有一个子节点，用待删除节点唯一的子节点或 None 来替换待删除节点
                    tmp = cur.left or cur.right
                else: # 待删除节点同时存在左右子节点，用待删除节点的后继节点（比当前节点大的最小的节点）来替换待删除节点
                    tmp = cur.right
                    tmp_prev: TreeNode[K, V] = cur # 后继节点的父节点
                    while tmp.left is not None:
                        tmp_prev = tmp
                        tmp = tmp.left
                    # 删除后继节点
                    if tmp_prev.left == tmp: # 后继节点是其父节点的左子节点
                        tmp_prev.left = tmp.right
                    else: # 后继节点是其父节点的右子节点
                        tmp_prev.right = tmp.right
                    # 用后继节点替换待删除节点（接替子节点关系）
                    tmp.left = cur.left
                    tmp.right = cur.right
                # 用后继节点替换待删除节点（接替父节点关系）
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
        raise KeyError(f"{key}在二叉搜索树中不存在")
    
    def get(self, key: K) -> V:
        """查询键值对

        Args:
            key (K): 待查询的键

        Raises:
            KeyError: 键在树中不存在

        Returns:
            V: 值
        """
        cur: Optional[TreeNode[K, V]] = self._root
        while cur is not None:
            if key < cur.key:
                cur = cur.left
            elif key > cur.key:
                cur = cur.right
            else:
                return cur.val
        raise KeyError(f"{key}在二叉搜索树中不存在")
    
    def get_root(self) -> Optional[TreeNode[K, V]]:
        """查看树的根节点

        Returns:
            Optional[TreeNode[K, V]]: 根节点
        """
        return self._root
    
    def keys(self) -> List[K]:
        """层序遍历查看所有键

        Returns:
            List[K]: 将树中的键以列表的形式返回
        """
        queue: ArrayQueue[TreeNode[K, V]] = ArrayQueue[TreeNode[K, V]]()
        result: List[Optional[K]] = [None] * self._size
        idx: int = 0
        if self._root is not None:
            queue.enqueue(item=self._root)
        while not queue.is_empty():
            cur: TreeNode[K, V] = queue.dequeue()
            result[idx] = cur.key
            idx += 1
            if cur.left is not None:
                queue.enqueue(item=cur.left)
            if cur.right is not None:
                queue.enqueue(item=cur.right)
        return result # type: ignore
        
    def values(self) -> List[V]:
        """层序遍历查看所有值

        Returns:
            List[V]: 将树中的值以列表的形式返回
        """
        queue: ArrayQueue[TreeNode[K, V]] = ArrayQueue[TreeNode[K, V]]()
        result: List[Optional[V]] = [None] * self._size
        idx: int = 0
        if self._root is not None:
            queue.enqueue(item=self._root)
        while not queue.is_empty():
            cur: TreeNode[K, V] = queue.dequeue()
            result[idx] = cur.val
            idx += 1
            if cur.left is not None:
                queue.enqueue(item=cur.left)
            if cur.right is not None:
                queue.enqueue(item=cur.right)
        return result # type: ignore
    
    def items(self) -> List[Tuple[K, V]]:
        """层序遍历查看所有键值对

        Returns:
            List[Tuple[K, V]]: 将树中的键值对元组以列表的形式返回
        """
        queue: ArrayQueue[TreeNode[K, V]] = ArrayQueue[TreeNode[K, V]]()
        result: List[Optional[Tuple[K, V]]] = [None] * self._size
        idx: int = 0
        if self._root is not None:
            queue.enqueue(item=self._root)
        while not queue.is_empty():
            cur: TreeNode[K, V] = queue.dequeue()
            result[idx] = (cur.key, cur.val)
            idx += 1
            if cur.left is not None:
                queue.enqueue(item=cur.left)
            if cur.right is not None:
                queue.enqueue(item=cur.right)
        return result # type: ignore

    def __getitem__(self, key: K) -> V:
        """查询键值对

        Args:
            key (K): 待查询的键

        Returns:
            V: 值
        """
        return self.get(key=key)
    
    def __setitem__(self, key: K, val: V) -> None:
        """新增或更新键值对

        Args:
            key (K): 键
            val (V): 值
        """
        self.put(key=key, val=val)

    def __delitem__(self, key: K) -> None:
        """删除键值对

        Args:
            key (K): 待删除的键

        Args:
            key (K): _description_
        """
        self.remove(key=key)
    
    def __contains__(self, key: K) -> bool:
        """树中是否存在指定键

        Args:
            val (K): 键

        Returns:
            bool: 键在树中是否存在
        """
        try:
            self.get(key=key)
            return True
        except KeyError:
            return False
        
    def __len__(self) -> int:
        """查看树中存储的键值对数量

        Returns:
            int: 树中存储的键值对数量
        """
        return self._size
    
    class Itr(Iterator):
        """该类配套的迭代器"""
        def __init__(self, outer: "BinarySearchTree[K, V]") -> None:
            """构造方法

            Args:
                outer (BinarySearchTree[K, V]): 指向外部类的引用
            """
            self.outer: BinarySearchTree[K, V] = outer # type: ignore
            self.queue: ArrayQueue[TreeNode[K, V]] = ArrayQueue[TreeNode[K, V]]() # type: ignore
            if self.outer._root is not None:
                self.queue.enqueue(item=self.outer._root)
        
        @override
        def __next__(self) -> K:
            """实现 Iterator 接口声明的 __next__ 方法（层序遍历）

            Raises:
                StopIteration: 停止迭代

            Returns:
                K: 
            """
            result: TreeNode[K, V] # type: ignore
            while not self.queue.is_empty():
                result = self.queue.dequeue()
                if result.left is not None:
                    self.queue.enqueue(item=result.left)
                if result.right is not None:
                    self.queue.enqueue(item=result.right)
                return result.key
            raise StopIteration

    def __iter__(self) -> Itr:
        """使自身可迭代

        Returns:
            Itr: 类内部实现的迭代器
        """
        return self.Itr(outer=self)
    


class AvlTreeNode(TreeNode[K, V]):
    """AVL树的节点"""
    @override
    def __init__(self, key: K, val: V) -> None:
        """构造方法

        Args:
            key (K): 键
            val (V): 值
        """
        self.key: K = key # 节点键
        self.val: V = val # 节点值
        self.left: Optional[AvlTreeNode[K, V]] = None # type: ignore # 左子节点引用
        self.right: Optional[AvlTreeNode[K, V]] = None # type: ignore # 右子节点引用
        self.parent: Optional[AvlTreeNode[K, V]] = None # 父节点的引用
        self.height: int = 0 # 规定叶子节点高度为 0
        self.balance_factor: int = 0 # 平衡因子

    def is_left_child(self) -> bool:
        """判断是否是左子节点

        Returns:
            bool: 是否是左子节点
        """
        return (self.parent is not None) and (self.parent.left is self)
    
    def is_right_child(self) -> bool:
        """判断是否是右子节点

        Returns:
            bool: 是否是右子节点
        """
        return (self.parent is not None) and (self.parent.right is self)
    

class AvlTree(Generic[K, V]):
    """AVL树"""
    def __init__(self) -> None:
        """构造方法（初始化一棵空的Avl树）"""
        self._root: Optional[AvlTreeNode[K, V]] = None
        self._size: int = 0

    @staticmethod # 静态方法
    def get_height(node: Optional[AvlTreeNode[K, V]]) -> int: # 因为需要计算空节点 None 的高度，所以不方便在 AvlTreeNode 类中定义
        """返回节点的高度（空节点高度为 -1 ，叶子节点高度为 0）

        Args:
            node (Optional[AvlTreeNode[K, V]]): 待查询节点

        Returns:
            int: 节点的高度
        """
        if node is not None:
            return node.height
        return -1
    
    @staticmethod # 静态方法
    def update_height(node: AvlTreeNode[K, V]) -> None:
        """更新节点的高度

        Args:
            node (AvlTreeNode[K, V]): 待更新节点
        """
        node.height = max(AvlTree.get_height(node=node.left), AvlTree.get_height(node=node.right)) + 1 # 节点高度等于最高子树高度 + 1
    
    @staticmethod # 静态方法
    def update_balance_factor(node: AvlTreeNode[K, V]) -> None:
        """更新节点的平衡因子

        Args:
            node (AvlTreeNode[K, V]): 待更新节点
        """
        node.balance_factor = AvlTree.get_height(node=node.left) - AvlTree.get_height(node=node.right)

    def left_rotate(self, node: AvlTreeNode[K, V]) -> AvlTreeNode[K, V]:
        """左旋
        将右子节点提升为子树的根节点；
        将旧根节点作为新根节点的左子节点；
        如果新根节点已经有一个左子节点，将其作为新左子节点（旧根节点）的右子节点。

        Args:
            node (AvlTreeNode[K, V]): 待旋转的子树的根节点

        Returns:
            AvlTreeNode[K, V]: 旋转后子树新的根节点
        """
        new_root: AvlTreeNode[K, V] = node.right # type: ignore # 子树新的根节点
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
        # 更新被调整过的节点的高度和平衡因子
        AvlTree.update_height(node=node)
        AvlTree.update_balance_factor(node=node)
        AvlTree.update_height(node=new_root)
        AvlTree.update_balance_factor(node=new_root)
        return new_root

    def right_rotate(self, node: AvlTreeNode[K, V]) -> AvlTreeNode[K, V]:
        """右旋
        将左子节点提升为子树的根节点；
        将旧根节点作为新根节点的右子节点；
        如果新根节点已经有一个右子节点，将其作为新右子节点（旧根节点）的左子节点。

        Args:
            node (AvlTreeNode[K, V]): 待旋转的子树的根节点

        Returns:
            AvlTreeNode[K, V]: 旋转后子树新的根节点
        """
        new_root: AvlTreeNode[K, V] = node.left # type: ignore # 子树新的根节点
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
        # 更新被调整过的节点的高度和平衡因子
        AvlTree.update_height(node=node)
        AvlTree.update_balance_factor(node=node)
        AvlTree.update_height(node=new_root)
        AvlTree.update_balance_factor(node=new_root)
        return new_root

    def reBalance(self, node: AvlTreeNode[K, V]) -> AvlTreeNode[K, V]:
        """再平衡

        Args:
            node (AvlTreeNode[K, V]): 待平衡的子树的根节点

        Returns:
            AvlTreeNode[K, V]: 平衡后子树新的根节点
        """
        new_root: AvlTreeNode[K, V]
        if node.balance_factor > 1:
            if node.left.balance_factor < 0: # type: ignore # 先围绕失衡节点的左子节点左旋，再围绕失衡节点右旋
                self.left_rotate(node=node.left) # type: ignore
                new_root = self.right_rotate(node=node)
            else: # 围绕失衡节点右旋
                new_root = self.right_rotate(node=node)
        elif node.balance_factor < -1:
            if node.right.balance_factor > 0: # type: ignore # 先围绕失衡节点的右子节点右旋，再围绕失衡节点左旋
                self.right_rotate(node=node.right) # type: ignore
                new_root = self.left_rotate(node=node)
            else: # 围绕失衡节点左旋
                new_root = self.left_rotate(node=node)
        return new_root # type: ignore

    def put(self, key: K, val: V) -> None:
        """新增或更新键值对

        Args:
            key (K): 键
            val (V): 值
        """
        if self._root is None: # 空树，直接在根节点存储新元素
            self._root = AvlTreeNode(key=key, val=val)
            self._size += 1
            return
        cur: Optional[AvlTreeNode[K, V]] = self._root
        prev: AvlTreeNode[K, V]
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
        # 此时prev 必已绑定，否则程序已经结束运行
        node: AvlTreeNode[K, V] = AvlTreeNode[K, V](key=key, val=val)
        if key < prev.key: # type: ignore
            prev.left = node # type: ignore
        else: # 不可能出现 key == prev.key 的情况
            prev.right = node # type: ignore
        node.parent = prev # type: ignore
        self._size += 1
        # 检查新插入节点的各个祖先节点是否失衡
        grand: Optional[AvlTreeNode[K, V]] = prev # type: ignore
        while grand is not None: # 叶子节点的高度和平衡因子无需更新
            AvlTree.update_height(node=grand)
            AvlTree.update_balance_factor(node=grand)
            if (grand.balance_factor > 1) or (grand.balance_factor < -1): # 离新插入节点最近的失衡节点
                self.reBalance(node=grand)
                break # 插入导致的失衡只需要调整一次
            grand = grand.parent

    def successor(self, node: AvlTreeNode[K, V]) -> AvlTreeNode[K, V]:
        """寻找给定节点的后继节点

        Args:
            node (AvlTreeNode[K, V]): 待查询节点

        Returns:
            AvlTreeNode[K, V]: 后继节点
        """
        result: Optional[AvlTreeNode[K, V]] = node.right # 后继节点
        if result is not None:
            while result.left is not None:
                result = result.left
        return result # type: ignore
    
    def remove(self, key: K) -> None:
        """删除键值对

        Args:
            key (K): 待删除的键

        Raises:
            KeyError: 待删除的键在树中不存在
        """
        cur: Optional[AvlTreeNode[K, V]] = self._root # 待删除节点
        while cur is not None:
            if key < cur.key:
                cur = cur.left
            elif key > cur.key:
                cur = cur.right
            else: # 定位到了待删除元素的位置
                # 寻找用于替换待删除节点的元素
                tmp: Optional[AvlTreeNode[K, V]]
                grand: Optional[AvlTreeNode[K, V]]
                if (cur.left is None) or (cur.right is None): # 至多只有一个子节点，用待删除节点唯一的子节点或 None 来替换待删除节点
                    tmp = cur.left or cur.right
                    grand = cur.parent # 实际被删除节点的父节点
                else: # 待删除节点同时存在左右子节点，用待删除节点的后继节点（比当前节点大的最小的节点）来替换待删除节点
                    tmp = self.successor(node=cur) # 后继节点
                    grand = tmp.parent # 实际被删除节点的父节点
                    # 删除后继节点
                    if tmp.is_left_child(): # 后继节点是其父节点的左子节点
                        tmp.parent.left = tmp.right # type: ignore
                    else: # 后继节点是其父节点的右子节点
                        tmp.parent.right = tmp.right # type: ignore
                    if tmp.right is not None: # 后继节点只可能有右子节点
                        tmp.right.parent = tmp.parent
                    # 用后继节点替换待删除节点（接替子节点关系）
                    tmp.left = cur.left
                    cur.left.parent = tmp
                    tmp.right = cur.right
                    cur.right.parent = tmp
                # 用后继节点替换待删除节点（接替父节点关系）
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
                # 检查实际被删除节点的各个祖先节点是否失衡
                while grand is not None:
                    AvlTree.update_height(node=grand)
                    AvlTree.update_balance_factor(node=grand)
                    if (grand.balance_factor > 1) or (grand.balance_factor < -1): # 离新插入节点最近的失衡节点
                        new_root = self.reBalance(node=grand)
                        grand = new_root.parent
                        continue # 删除导致的失衡可能要调整多次
                    grand = grand.parent
                return
        raise KeyError(f"{key}在AVL树中不存在")

    def get(self, key: K) -> V:
        """查询键值对

        Args:
            key (K): 待查询的键

        Raises:
            KeyError: 键在树中不存在

        Returns:
            V: 值
        """
        cur: Optional[AvlTreeNode[K, V]] = self._root
        while cur is not None:
            if key < cur.key:
                cur = cur.left
            elif key > cur.key:
                cur = cur.right
            else:
                return cur.val
        raise KeyError(f"{key}在AVL树中不存在")
    
    def get_root(self) -> Optional[AvlTreeNode[K, V]]:
        """查看树的根节点

        Returns:
            Optional[TreeNode[K, V]]: 根节点
        """
        return self._root
    
    def keys(self) -> List[K]:
        """层序遍历查看所有键

        Returns:
            List[K]: 将树中的键以列表的形式返回
        """
        queue: ArrayQueue[AvlTreeNode[K, V]] = ArrayQueue[AvlTreeNode[K, V]]()
        result: List[Optional[K]] = [None] * self._size
        idx: int = 0
        if self._root is not None:
            queue.enqueue(item=self._root)
        while not queue.is_empty():
            cur: AvlTreeNode[K, V] = queue.dequeue()
            result[idx] = cur.key
            idx += 1
            if cur.left is not None:
                queue.enqueue(item=cur.left)
            if cur.right is not None:
                queue.enqueue(item=cur.right)
        return result # type: ignore
        
    def values(self) -> List[V]:
        """层序遍历查看所有值

        Returns:
            List[V]: 将树中的值以列表的形式返回
        """
        queue: ArrayQueue[AvlTreeNode[K, V]] = ArrayQueue[AvlTreeNode[K, V]]()
        result: List[Optional[V]] = [None] * self._size
        idx: int = 0
        if self._root is not None:
            queue.enqueue(item=self._root)
        while not queue.is_empty():
            cur: AvlTreeNode[K, V] = queue.dequeue()
            result[idx] = cur.val
            idx += 1
            if cur.left is not None:
                queue.enqueue(item=cur.left)
            if cur.right is not None:
                queue.enqueue(item=cur.right)
        return result # type: ignore
    
    def items(self) -> List[Tuple[K, V]]:
        """层序遍历查看所有键值对

        Returns:
            List[Tuple[K, V]]: 将树中的键值对元组以列表的形式返回
        """
        queue: ArrayQueue[AvlTreeNode[K, V]] = ArrayQueue[AvlTreeNode[K, V]]()
        result: List[Optional[Tuple[K, V]]] = [None] * self._size
        idx: int = 0
        if self._root is not None:
            queue.enqueue(item=self._root)
        while not queue.is_empty():
            cur: AvlTreeNode[K, V] = queue.dequeue()
            result[idx] = (cur.key, cur.val)
            idx += 1
            if cur.left is not None:
                queue.enqueue(item=cur.left)
            if cur.right is not None:
                queue.enqueue(item=cur.right)
        return result # type: ignore

    def __getitem__(self, key: K) -> V:
        """查询键值对

        Args:
            key (K): 待查询的键

        Returns:
            V: 值
        """
        return self.get(key=key)
    
    def __setitem__(self, key: K, val: V) -> None:
        """新增或更新键值对

        Args:
            key (K): 键
            val (V): 值
        """
        self.put(key=key, val=val)

    def __delitem__(self, key: K) -> None:
        """删除键值对

        Args:
            key (K): 待删除的键

        Args:
            key (K): _description_
        """
        self.remove(key=key)
    
    def __contains__(self, key: K) -> bool:
        """树中是否存在指定键

        Args:
            val (K): 键

        Returns:
            bool: 键在树中是否存在
        """
        try:
            self.get(key=key)
            return True
        except KeyError:
            return False
        
    def __len__(self) -> int:
        """查看树中存储的键值对数量

        Returns:
            int: 树中存储的键值对数量
        """
        return self._size
    
    class Itr(Iterator):
        """该类配套的迭代器"""
        def __init__(self, outer: "AvlTree[K, V]") -> None:
            """构造方法

            Args:
                outer (AvlTree[K, V]): 指向外部类的引用
            """
            self.outer: AvlTree[K, V] = outer # type: ignore
            self.queue: ArrayQueue[AvlTreeNode[K, V]] = ArrayQueue[AvlTreeNode[K, V]]() # type: ignore
            if self.outer._root is not None:
                self.queue.enqueue(item=self.outer._root)
        
        @override
        def __next__(self) -> K:
            """实现 Iterator 接口声明的 __next__ 方法（层序遍历）

            Raises:
                StopIteration: 停止迭代

            Returns:
                K: 
            """
            result: AvlTreeNode[K, V] # type: ignore
            while not self.queue.is_empty():
                result = self.queue.dequeue()
                if result.left is not None:
                    self.queue.enqueue(item=result.left)
                if result.right is not None:
                    self.queue.enqueue(item=result.right)
                return result.key
            raise StopIteration

    def __iter__(self) -> Itr:
        """使自身可迭代

        Returns:
            Itr: 类内部实现的迭代器
        """
        return self.Itr(outer=self)



# 二叉树的遍历

# 层序遍历
def level_order(root: Optional[TreeNode[K, V]]) -> LinkedList[K]:
    """层序遍历（即广度优先遍历，从顶部到底部逐层遍历二叉树）

    Args:
        root (Optional[TreeNode[K, V]]): 根节点

    Returns:
        LinkedList[K]: 将树中的键以链表的形式返回
    """
    queue: ArrayQueue[TreeNode[K, V]] = ArrayQueue[TreeNode[K, V]]()
    result: LinkedList[K] = LinkedList[K]()
    if root is not None:
        queue.enqueue(item=root)
    while not queue.is_empty():
        cur: TreeNode[K, V] = queue.dequeue()
        result.append(val=cur.key)
        if cur.left is not None:
            queue.enqueue(item=cur.left)
        if cur.right is not None:
            queue.enqueue(item=cur.right)
    return result



# 前序、中序和后序遍历都属于深度优先遍历
# 前中后指的是每一层的“根节点”；遍历一定是先左后右的，所以前中后序分别是：中左右、左中右、左右中
def pre_order(root: Optional[TreeNode[K, V]]) -> LinkedList[K]:
    """前序遍历

    Args:
        root (Optional[TreeNode[K, V]]): 根节点

    Returns:
        LinkedList[K]: 将树中的键以链表的形式返回
    """
    result: LinkedList[K] = LinkedList[K]()
    def pre_order_helper(root: Optional[TreeNode[K, V]]) -> None:
        if root is None:
            return
        # 访问优先级：根节点 -> 左子树 -> 右子树
        result.append(val=root.key)
        pre_order_helper(root=root.left)
        pre_order_helper(root=root.right)
    pre_order_helper(root=root)
    return result


def in_order(root: Optional[TreeNode[K, V]]) -> LinkedList[K]:
    """中序遍历

    Args:
        root (Optional[TreeNode[K, V]]): 根节点

    Returns:
        LinkedList[K]: 将树中的键以链表的形式返回
    """
    result: LinkedList[K] = LinkedList[K]()
    def in_order_helper(root: Optional[TreeNode[K, V]]) -> None:
        if root is None:
            return
        # 访问优先级：左子树 -> 根节点 -> 右子树
        in_order_helper(root=root.left)
        result.append(val=root.key)
        in_order_helper(root=root.right)
    in_order_helper(root=root)
    return result


def post_order(root: Optional[TreeNode[K, V]]) -> LinkedList[K]:
    """后序遍历

    Args:
        root (Optional[TreeNode[K, V]]): 根节点

    Returns:
        LinkedList[K]: 将树中的键以链表的形式返回
    """
    result: LinkedList[K] = LinkedList[K]()
    def post_order_helper(root: Optional[TreeNode[K, V]]) -> None:
        if root is None:
            return
        # 访问优先级：左子树 -> 右子树 -> 根节点
        post_order_helper(root=root.left)
        post_order_helper(root=root.right)
        result.append(val=root.key)
    post_order_helper(root=root)
    return result



if __name__ == "__main__":
    myTree: BinarySearchTree[int, str] = BinarySearchTree[int, str]()
    for i in [9, 5, 17, 3, 7, 15, 20, 1, 4, 6, 8, 10, 16, 18, 22]:
        myTree.put(key=i, val=str(object=i))
    print("层序遍历", level_order(root=myTree.get_root()).to_list())
    l1:LinkedList[int] = pre_order(root=myTree.get_root())
    print("前序遍历", l1.to_list())
    l2:LinkedList[int] = in_order(root=myTree.get_root())
    print("中序遍历", l2.to_list())
    l3:LinkedList[int] = post_order(root=myTree.get_root())
    print("后序遍历", l3.to_list())

    print("AVL树")
    avl: AvlTree[int, str] = AvlTree[int, str]()
    d: List[int] = [14, 9, 5, 17, 11, 12, 7, 19, 16, 27, 8, 18, 23]
    for i in d:
        avl.put(key=i, val=str(object=i))
    print("层序遍历", level_order(root=avl.get_root()).to_list())
    avl.remove(key=5)
    print("层序遍历", level_order(root=avl.get_root()).to_list())
    l: LinkedList[int] = in_order(root=avl.get_root())
    print("中序遍历", l.to_list())
    for i in avl:
        print(i)
    print(avl.keys())
    print(avl.values())
    print(avl.items())