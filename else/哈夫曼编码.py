import sys
from pathlib import Path

sys.path.append(str(object=Path(__file__).parent.parent)) # Path(__file__) 获取的当前 py 文件的路径

from Heap import MinPriorityQueue
from HashMap import HashMapChaining
from Stack import ArrayStack
from Array import DynamicArray



class HuffmanTreeNode:
    '''哈夫曼树的节点'''
    def __init__(self, name: str = None, weight: int = None) -> None:
        '''拥有 obj 和 attr 属性的对象即可用于构建 MinPriorityQueue'''
        self.obj: str = name # 节点的名字编号
        self.attr: int = weight # 节点的权重
        self.left_child: HuffmanTreeNode | None = None # 左子节点
        self.right_child: HuffmanTreeNode | None = None # 右子节点
        self.parent: HuffmanTreeNode | None = None # 父节点

    def is_left_child(self) -> bool:
        '''判断是父节点的左子节点'''
        return (self.parent is not None) and (self.parent.left_child == self)
    
    def is_right_child(self) -> bool:
        '''判断是父节点的右子节点'''
        return (self.parent is not None) and (self.parent.right_child == self)



class HuffmanTree:
    '''哈夫曼树'''
    def __init__(self, text: str) -> None:
        '''构造哈夫曼树'''
        self.map: HashMapChaining = HashMapChaining() # Unicode 编码到字符之间的映射
        self.counter : HashMapChaining = HashMapChaining() # 统计每个字符出现的次数
        for s in text:
            code: int = ord(s)
            self.map[code] = s
            try:
                self.counter[code] += 1
            except KeyError:
                self.counter[code] = 1
        self.leaves: DynamicArray[HuffmanTreeNode | None] = DynamicArray(capacity=len(self.counter))
        for i in self.counter:
            self.leaves.append(item=HuffmanTreeNode(name=self.map[i], weight=self.counter[i]))
        self.min_priority_queue: MinPriorityQueue = MinPriorityQueue(data=self.leaves) # 字符按其出现次数进行比较构成的优先队列
        '''权重越小的字符离根节点越远，其对应的哈夫曼编码也就越长'''
        while len(self.min_priority_queue) != 1:
            left_node: HuffmanTreeNode = self.min_priority_queue.dequeue()
            right_node: HuffmanTreeNode = self.min_priority_queue.dequeue()
            parent_node: HuffmanTreeNode = HuffmanTreeNode(weight=left_node.attr+right_node.attr)
            left_node.parent = right_node.parent = parent_node
            parent_node.left_child, parent_node.right_child = left_node, right_node
            self.min_priority_queue.enqueue(item=parent_node)
    
    def get_code(self, char: str) -> str:
        '''获取单个字符的哈夫曼编码'''
        for leaf in self.leaves:
            if leaf.obj == char:
                stack: ArrayStack = ArrayStack()
                while leaf.parent is not None:
                    if leaf.is_left_child():
                        stack.push(item='0')
                    else:
                        stack.push(item='1')
                    leaf = leaf.parent
                code: str = str()
                while not stack.is_empty():
                    code += stack.pop()
                return code
        raise KeyError(f'{char}不是哈夫曼树的叶子结点')



if __name__ == '__main__':
    text: str = 'aaaabbbccd'
    h: HuffmanTree = HuffmanTree(text=text)
    for i in set(text):
        print(i, h.get_code(char=i))