from typing import Generic, TypeVar, Sequence
from HashMap import HashMapOpenAddressing as HashMap



T = TypeVar(
            name="T", 
            # covariant=True
        ) # 声明一个类型参数，不宜对其进行 type hints

class UnionFindSet(Generic[T]):
    """并查集"""
    def __init__(self, arr: Sequence[T]) -> None:
        """每个节点的祖先节点设为自身

        Args:
            arr (Sequence[T]): 节点序列
        """
        self.ancestors: HashMap[T, T] = HashMap[T, T]() # 记录每个节点的祖先节点
        self.offspring: HashMap[T, int] = HashMap[T, int]() # 记录每个节点其后代节点的个数，只有祖先节点为自身的节点的后代节点个数才是准确的
        for i in arr:
            self.ancestors[i] = i
            self.offspring[i] = 0
    
    def find(self, node: T) -> T:
        """递归查找祖先节点，并进行路径压缩

        Args:
            node (T): 待查询节点

        Returns:
            T: 祖先节点
        """
        ancestor: T = self.ancestors[node]
        if ancestor != node:
            ancestor = self.find(node=ancestor) # 真正的祖先节点
            if self.ancestors[node] != ancestor:
                # 更新真正的祖先节点
                self.offspring[self.ancestors[node]] -= 1 # 原本记录的祖先节点后代数减 1
                self.ancestors[node] = ancestor
                self.offspring[ancestor] += 1 #  真正的的祖先节点后代数加 1
        return ancestor # 递归的基本情况，self.ancestors[node] == node
    
    def is_relative(self, node1: T, node2: T) -> bool:
        """是否有相同的祖先

        Args:
            node1 (T): 待查询节点1
            node2 (T): 待查询节点2

        Returns:
            bool: 是否有相同的祖先
        """
        return self.find(node=node1) == self.find(node=node2)
    
    def union(self, node1: T, node2: T) -> None:
        """合并，将后代少的祖先节点作为后代多的祖先节点的后代

        Args:
            node1 (T): 待合并的祖先节点1
            node2 (T): 待合并的祖先节点2
        """
        ancestor1: T = self.find(node=node1)
        ancestor2: T = self.find(node=node2)
        if ancestor1 != ancestor2:
            if self.offspring[ancestor1] >= self.offspring[ancestor2]:
                self.ancestors[ancestor2] = ancestor1
                self.offspring[ancestor1] += self.offspring[ancestor2]
            else:
                self.ancestors[ancestor1] = ancestor2
                self.offspring[ancestor2] += self.offspring[ancestor1]



if __name__ == "__main__":
    ufs: UnionFindSet[int] = UnionFindSet[int](arr=range(1, 5))
    ufs.union(node1=1, node2=2)
    ufs.union(node1=2, node2=3)
    ufs.union(node1=3, node2=4)
    print(f"节点：{4}，祖先节点：{ufs.find(node=4)}")
    for i in range(1, 5):
        print("-------")
        print(f"节点：{i}，后代节点个数：{ufs.offspring[i]}")
        print(f"节点：{i}，祖先节点：{ufs.ancestors[i]}")