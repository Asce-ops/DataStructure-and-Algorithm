from typing import Generic, List, Optional, Tuple, TypeVar, Hashable
from copy import deepcopy

from HashMap import HashMapOpenAddressing as HashMap
from Queue import ArrayQueue
from Array import DynamicArray
from LinkedList import LinkedList
from UnionFindSet import UnionFindSet
from Stack import ArrayStack



T = TypeVar(name="T", bound=Hashable) # 声明一个类型参数，不宜对其进行 type hints

class Vertex(Generic[T]):
    """顶点"""
    def __init__(self, val: T) -> None:
        """构造方法

        Args:
            val (T): 顶点要存储的对象
        """
        self.val: T = val # 顶点的唯一标识
        self.from_edges: HashMap[T, int] = HashMap[T, int]() # 入边，{顶点的唯一标识：权重}
        self.to_edges: HashMap[T, int] = HashMap[T, int]() # 出边，{顶点的唯一标识：权重}
        self.from_degree: int = 0 # 入度
        self.to_degree: int = 0 # 出度

    def get_from_degree(self) -> int:
        """查询入度

        Returns:
            int: 当前顶点的入度
        """
        return self.from_degree
    
    def get_to_degree(self) -> int:
        """查询出度

        Returns:
            int: 当前顶点的出度
        """
        return self.to_degree
    
    def get_from_edges(self) -> HashMap[T, int]:
        """查询入边

        Returns:
            HashMap[int, int]: 当前顶点的入边
        """
        return self.from_edges
    
    def get_to_edges(self) -> HashMap[T, int]:
        """查询出边

        Returns:
            HashMap[int, int]: 当前顶点的出边
        """
        return self.to_edges



class Graph(Generic[T]):
    """图"""
    def __init__(self) -> None:
        """构造方法"""
        self.vertexes: HashMap[T, Vertex] = HashMap[T, Vertex]() # {顶点的唯一标识：顶点}
        self.vertexes_num: int = 0 # 顶点数量
        self.edges_num: int = 0 # 边的数量

    def add_vertex(self, vertex: T) -> None:
        """添加顶点

        Args:
            vertex (T): 待添加的顶点
        """
        if vertex in self.vertexes:
            return
        self.vertexes[vertex] = Vertex(val=vertex)
        self.vertexes_num += 1

    def set_edge(self, from_vertex: T, to_vertex: T, weight: int = 1) -> None:
        """添加或更新边

        Args:
            from_vertex (T): 起点
            to_vertex (T): 终点
            weight (int, optional): 边权. Defaults to 1.
        """
        if from_vertex not in self.vertexes: # 边所连接的顶点不存在，添加顶点
            self.add_vertex(vertex=from_vertex)
        if to_vertex not in self.vertexes:
            self.add_vertex(vertex=to_vertex)
        # 更新顶点的出入边和出入度
        if to_vertex not in self.vertexes[from_vertex].to_edges: # 则 from_vertex not in self.vertexes[to_vertex].from_edges
            # 边不存在
            self.vertexes[from_vertex].to_degree += 1
            self.vertexes[to_vertex].from_degree += 1
            self.edges_num += 1
        # 边存在，更新边权
        self.vertexes[from_vertex].to_edges[to_vertex] = weight
        self.vertexes[to_vertex].from_edges[from_vertex] = weight

    def remove_vertex(self, vertex: T) -> None:
        """删除顶点

        Args:
            vertex (T): 待删除顶点

        Raises:
            ValueError: 待删除顶点在图中不存在
        """
        v: T
        for v in self.vertexes: # type: ignore
            if v == hash(vertex): # 定位到待删除的顶点
                if v in self.vertexes[v].to_edges: # 有指向自己的边，则入边和出边中有一条重复
                    self.edges_num -= (self.vertexes[v].to_degree + self.vertexes[v].from_degree - 1)
                else:
                    self.edges_num -= (self.vertexes[v].to_degree + self.vertexes[v].from_degree)
                # 更新和待删除顶点相连的顶点的出入边和出入度
                i: T
                for i in self.vertexes[v].to_edges: # type: ignore
                    del self.vertexes[i].from_edges[v]
                    self.vertexes[i].from_degree -= 1
                for i in self.vertexes[v].from_edges: # type: ignore
                    del self.vertexes[i].to_edges[v]
                    self.vertexes[i].to_degree -= 1
                del self.vertexes[v]
                self.vertexes_num -= 1
                return
        raise ValueError(f"顶点{vertex}在图中不存在")
    
    def remove_edge(self, from_vertex: T, to_vertex: T) -> None:
        """删除边

        Args:
            from_vertex (T): 待删除边的起点
            to_vertex (T): 待删除边的终点

        Raises:
            ValueError: 待删除边在图中不存在
        """
        if (from_vertex in self.vertexes) and (to_vertex in self.vertexes):
            if to_vertex in self.vertexes[from_vertex].to_edges:
                del self.vertexes[from_vertex].to_edges[to_vertex]
                self.vertexes[from_vertex].to_degree -= 1
                del self.vertexes[to_vertex].from_edges[from_vertex]
                self.vertexes[to_vertex].from_degree -= 1
                self.edges_num -= 1
                return
        raise ValueError(f"边{from_vertex} --> {to_vertex}在图中不存在")
    
    def get(self, vertex: T) -> Vertex:
        """返回对象所在的顶点

        Args:
            vertex (T): 顶点中存储的对象

        Returns:
            Vertex: 对象所在的顶点
        """
        return self.vertexes[vertex]
    
    def get_weight(self, from_vertex: T, to_vertex: T) -> int:
        """查询边的权重

        Args:
            from_vertex (T): 待查询边的起点
            to_vertex (T): 待查询边的终点

        Raises:
            ValueError: 待查询边在图中不存在

        Returns:
            int: 待查询边的边权
        """
        if from_vertex in self.vertexes:
            try:
                return self.vertexes[from_vertex].to_edges[to_vertex]
            except KeyError:
                pass
        raise ValueError(f"边{from_vertex} --> {to_vertex}在图中不存在")
    
    def __getitem__(self, vertex: T) -> Vertex:
        """返回对象所在的顶点

        Args:
            vertex (T): 顶点中存储的对象

        Returns:
            Vertex: 对象所在的顶点
        """
        return self.get(vertex=vertex)
    
    def __len__(self) -> int:
        """查看顶点的数量

        Returns:
            int: 顶点的数量
        """
        return self.vertexes_num
    
    def size(self) -> int:
        """查看边的数量

        Returns:
            int: 边的数量
        """
        return self.edges_num
    
    def __contains__(self, vertex: T) -> bool:
        """判断顶点是否在图中

        Args:
            vertex (T): 待查询的对象

        Returns:
            bool: 顶点是否在图中
        """
        return vertex in self.vertexes



# 不重不漏地访问图中的所有顶点
def graph_bfs(graph: Graph[T], start_vertex: T) -> DynamicArray[T]:
    """广度优先遍历

    Args:
        graph (Graph[T]): 图
        start_vertex (T): 起点

    Raises:
        ValueError: 起点对象在图中不存在

    Returns:
        DynamicArray[T]: 将图中的顶点以动态列表的形式返回
    """
    if start_vertex not in graph:
        raise ValueError(f"顶点{start_vertex}在图中不存在")
    result: DynamicArray[T] = DynamicArray[T]()
    visited: HashMap[T, None] = HashMap[T, None]() # 用哈希表来实现集合
    queue: ArrayQueue[Vertex] = ArrayQueue[Vertex]()
    queue.enqueue(item=graph[start_vertex])
    visited.put(key=start_vertex, val=None) # 需要在入队时添加，如果在出队时添加可能导致顶点重复入队
    while len(queue) > 0:
        cur: Vertex = queue.dequeue()
        result.append(item=cur.val)
        i: T
        for i in cur.get_to_edges(): # type: ignore
            if i not in visited:
                queue.enqueue(item=graph[i])
                visited.put(key=i, val=None)
    return result


def graph_dfs(graph: Graph[T], start_vertex: T) -> DynamicArray[T]:
    """深度优先遍历

    Args:
        graph (Graph[T]): 图
        start_vertex (T): 起点

    Raises:
        ValueError: 起点对象在图中不存在

    Returns:
        DynamicArray[T]: 将图中的顶点以动态列表的形式返回
    """
    if start_vertex not in graph:
        raise ValueError(f"顶点{start_vertex}在图中不存在")
    result: DynamicArray[T] = DynamicArray[T]()
    visited: HashMap[T, None] = HashMap[T, None]() # 用哈希表来实现集合
    def dfs(vertex: T) -> None:
        result.append(item=vertex)
        visited.put(key=vertex, val=None)
        i: T
        for i in graph[vertex].get_to_edges(): # type: ignore
            if i not in visited:
                dfs(vertex=i)
    dfs(vertex=start_vertex)
    return result



# 最短路径
def dijkstra(graph: Graph[T], start_vertex: T) -> Tuple[HashMap[T, int], HashMap[T, LinkedList[T]]]:
    """迪杰斯特拉算法确定非负加权图的单源最短路径

    Args:
        graph (Graph[T]): 图
        start_vertex (T): 起点

    Returns:
        Tuple[HashMap[T, int], HashMap[T, LinkedList[T]]]: 前往其他顶点的最短距离和最短路径
    """
    unvisited_vertexes: HashMap[T, int] = HashMap[T, int]()
    for vertex in graph.vertexes:
        # 初始化所有节点距离为无穷大
        unvisited_vertexes[vertex] = float("inf") # type: ignore
    unvisited_vertexes[start_vertex] = 0 # 起始节点距离为0
    shortest_paths: HashMap[T, LinkedList[T]] = HashMap[T, LinkedList[T]]()
    shortest_distances: HashMap[T, int] = HashMap[T, int]()
    shortest_paths[start_vertex], shortest_distances[start_vertex] = LinkedList[T](), 0
    while len(unvisited_vertexes) > 0:
        current_vertex: T = min(unvisited_vertexes, key=unvisited_vertexes.get) # type: ignore # 找到未访问节点中距离最近的节点
        current_distance: int = unvisited_vertexes[current_vertex]
        to_edges: HashMap[T ,int] = graph[current_vertex].get_to_edges()
        neighbor: T
        for neighbor in to_edges: # type: ignore
            if neighbor in unvisited_vertexes: # 已访问过的节点跳过
                new_distance: int = current_distance + to_edges[neighbor]
                if new_distance < unvisited_vertexes[neighbor]: # 如果找到更短路径，更新
                    unvisited_vertexes[neighbor] = new_distance
                    shortest_distances[neighbor] = new_distance
                    shortest_paths[neighbor] = deepcopy(x=shortest_paths[current_vertex])
                    shortest_paths[neighbor].append(val=neighbor)
        del unvisited_vertexes[current_vertex] # 当前节点已访问过，从未访问节点中删除
    return (shortest_distances, shortest_paths)



def weight_matrix(graph: Graph[int]) -> List[List[int]]:
    """返回图的距离矩阵（顶点必须以连续的非负整数表示）

    Args:
        graph (Graph[int]): 图

    Returns:
        List[List[int]]: 距离矩阵
    """
    result: List[List[int]] = [[float("inf")] * len(graph) for _ in range(len(graph))] # type: ignore # result[i][j] 为无穷表示不存在从 i 到 j 的边
    from_vertex: int
    for from_vertex in graph.vertexes: # type: ignore
        result[from_vertex][from_vertex] = 0 # 没有自身到自身的边则设为 0
        to_edges: HashMap[int ,int] = graph[from_vertex].get_to_edges()
        to_vertex: int
        for to_vertex in to_edges: # type: ignore
            result[from_vertex][to_vertex] = to_edges[to_vertex]
    return result



def floyd(graph: Graph[int]) -> List[Tuple[Tuple[int, int], int, LinkedList[int]]]:
    """弗洛伊德算法确定非负加权图的多源最短路径（顶点必须以连续的非负整数表示）

    Args:
        graph (Graph[int]): 图

    Returns:
        List[Tuple[Tuple[int, int], int, LinkedList[int]]]: 每一个元素表示((起点, 终点), 最短距离, 最短路径)元组
    """
    n: int = len(graph)
    D: List[List[int]] = weight_matrix(graph=graph) # D[i][j] 表示从 i 到 j 的最短距离
    P: List[List[Optional[int]]] = [[None] * n for _ in range(n)] # P[i][j] 表示从 i 到 j 的最短路径中 j 的前一个顶点
    from_vertex: int
    for from_vertex in graph.vertexes: # type: ignore
        to_edges: HashMap[int ,int] = graph[from_vertex].get_to_edges()
        to_vertex: int
        for to_vertex in to_edges: # type: ignore
            P[from_vertex][to_vertex] = from_vertex
    middle_vertex: int
    for middle_vertex in range(n): # 依次将每个顶点作为允许经过的点，更新最短路径
        for from_vertex in range(n):
            if from_vertex == middle_vertex:
                continue
            for to_vertex in range(n):
                if (to_vertex == middle_vertex) or (to_vertex == from_vertex):
                    continue
                if D[from_vertex][middle_vertex] + D[middle_vertex][to_vertex] < D[from_vertex][to_vertex]:
                    D[from_vertex][to_vertex] = D[from_vertex][middle_vertex] + D[middle_vertex][to_vertex]
                    P[from_vertex][to_vertex] = P[middle_vertex][to_vertex]
    # 返回任意两点间的最短距离和对应路径
    result: List[Optional[Tuple[Tuple[int, int], int, LinkedList[int]]]] = [None] * n**2
    idx: int = 0
    for from_vertex in range(n):
        for to_vertex in range(n):
            path: LinkedList[int] = LinkedList[int]()
            distance: int | float = D[from_vertex][to_vertex]
            # 确定最短距离对应的路径
            if (distance == 0) or (distance == float("inf")):
                result[idx] = ((from_vertex, to_vertex), distance, path)
            else:
                stack: ArrayStack[int] = ArrayStack[int]() # 存储最短路径经过的每一个顶点
                stack.push(item=to_vertex)
                middle_vertex = P[from_vertex][to_vertex] # type: ignore
                stack.push(item=middle_vertex)
                while from_vertex != middle_vertex:
                    middle_vertex = P[from_vertex][middle_vertex] # type: ignore
                    stack.push(item=middle_vertex)
                while len(stack) > 0:
                    path.append(val=stack.pop())
                    result[idx] = ((from_vertex, to_vertex), distance, path)
            idx += 1
    return result # type: ignore



# 最小生成树：连通图（任意顶点 v 到顶点 w 之间都存在路径）中的一个子图，使得所有顶点都相互连通，且总边权和最小
def prim(graph: Graph[T]) -> Graph[T]:
    """普里姆算法最小生成树：
    1. 首先选择一个起始节点，以这个节点将图分成两个集合。一个已选集合，一个未选集合，把起始节点加入已选集合；
    2. 从未选节点集合中选择距离已选节点集合最近的节点，并将其加入已选节点集合；
    3. 不断重复步骤 2，直到所有节点都被加入到已选节点集合中，形成最小生成树。

    Args:
        graph (Graph[T]): 图

    Returns:
        Graph[T]: 最小生成树（子图）
    """
    selected: HashMap[T, None] = HashMap[T, None]() # 模拟集合，{vertex}
    first_vertex: T = next(iter(graph.vertexes)) # type: ignore
    selected.put(key=first_vertex, val=None) # 从第一个顶点开始
    unselected: List[T] = graph.vertexes.keys()
    unselected.remove(first_vertex)
    used_edges: LinkedList[Tuple[T, T, int]] = LinkedList[Tuple[T, T, int]]() # 用于组成最小生成树的边
    while len(unselected) > 0:
        minimum: int | float = float("inf")
        from_vertex: T
        to_vertex: T
        # 从未选中部分找到距离已选中部分最近的顶点
        vertex: T
        for vertex in selected: # type: ignore
            to_edges: HashMap[T, int] = graph[vertex].get_to_edges()
            neighbor: T
            for neighbor in to_edges: # type: ignore
                if neighbor in unselected:
                    if to_edges[neighbor] < minimum: # 找到权值最小的边
                        minimum = to_edges[neighbor]
                        from_vertex = vertex
                        to_vertex = neighbor
        used_edges.append(val=(from_vertex, to_vertex, minimum)) # type: ignore
        selected.put(key=to_vertex, val=None) # type: ignore
        unselected.remove(to_vertex) # type: ignore
    # 利用组成最小生成树的边构建一个子图
    minimum_spanning_tree: Graph[T] = Graph[T]()
    edge: Tuple[T, T, int]
    for edge in used_edges: # type: ignore
        minimum_spanning_tree.set_edge(from_vertex=edge[0], to_vertex=edge[1], weight=edge[2])
        minimum_spanning_tree.set_edge(from_vertex=edge[1], to_vertex=edge[0], weight=edge[2])
    return minimum_spanning_tree



def kruskal(graph: Graph[T]) -> Graph[T]:
    """克鲁斯卡尔算法最小生成树：
    取出所有的边，按其权值从小到大的顺序排列，
    然后不断取出权值最小的边放入图中，一共取顶点数减 1 条边。
    但是每次放入一条边都要判断是否形成了环；
    如果没有形成环，则将该边纳入最小生成树中，
    如果形成了环，则舍弃这条边，继续取下一条边。

    Args:
        graph (Graph[T]): 图

    Returns:
        Graph[T]: 最小生成树（子图）
    """
    used_edges: LinkedList[Tuple[T, T, int]] = LinkedList[Tuple[T, T, int]]() # 用于组成最小生成树的边
    ufs: UnionFindSet[T] = UnionFindSet[T](arr=graph.vertexes.keys()) # 初始化并查集
    # 获取所有的边
    edges: List[Optional[Tuple[T, T, int]]] = [None] * graph.size()
    idx: int = 0
    from_vertex: T
    for from_vertex in graph.vertexes: # type: ignore
        to_edges: HashMap[T, int] = graph[from_vertex].get_to_edges()
        to_vertex: T
        for to_vertex in to_edges: # type: ignore
            edges[idx] = (from_vertex, to_vertex, to_edges[to_vertex])
            idx += 1
    edges.sort(key=lambda edge: edge[2], reverse=True) # type: ignore # 将所有的边按照权重降序排序
    while len(used_edges) < len(graph) - 1:
        weight: int
        from_vertex, to_vertex, weight = edges.pop() # type: ignore
        if not ufs.is_relative(node1=from_vertex, node2=to_vertex): # from_vertex 和 to_vertex 是否已经连通
            ufs.union(node1=from_vertex, node2=to_vertex)
            used_edges.append(val=(from_vertex, to_vertex, weight))
    # 利用组成最小生成树的边构建一个子图
    minimum_spanning_tree: Graph[T] = Graph[T]()
    edge: Tuple[T, T, int]
    for edge in used_edges: # type: ignore
        minimum_spanning_tree.set_edge(from_vertex=edge[0], to_vertex=edge[1], weight=edge[2])
        minimum_spanning_tree.set_edge(from_vertex=edge[1], to_vertex=edge[0], weight=edge[2])
    return minimum_spanning_tree



def topological_sorting(graph: Graph[T]) -> LinkedList[T]:
    """ 拓扑排序是一个有向无环图（环是一条只有第一个和最后一个顶点重复的非空路径）的所有顶点的线性序列，并满足以下两个条件：
    1. 每个顶点出现且只出现一次；
    2. 若存在一条从顶点 A 到顶点 B 的路径，则在序列中顶点 A 出现在顶点 B 的前面。

    Args:
        graph (Graph[T]): 图

    Raises:
        AttributeError: 有环图

    Returns:
        LinkedList[T]: 所有顶点的线性序列
    """
    graphCopy: Graph[T] = deepcopy(x=graph)
    result: LinkedList[T] = LinkedList[T]()
    for _ in range(len(graphCopy)):
        vertex: T
        for vertex in graphCopy.vertexes: # type: ignore
            if graphCopy.vertexes[vertex].from_degree == 0:
                result.append(val=vertex)
                graphCopy.remove_vertex(vertex=vertex)
                break
        else:
            raise AttributeError("图中存在环，找不到入度为 0 的顶点")
    return result



if __name__ == "__main__":
    # g: Graph[int] = Graph[int]()
    # g.add_vertex(vertex=1)
    # g.add_vertex(vertex=2)
    # g.add_vertex(vertex=3)
    # g.set_edge(from_vertex=1, to_vertex=2)
    # g.set_edge(from_vertex=1, to_vertex=4)
    # g.set_edge(from_vertex=2, to_vertex=4)
    # g.set_edge(from_vertex=2, to_vertex=3)
    # g.set_edge(from_vertex=4, to_vertex=5)
    # g.set_edge(from_vertex=5, to_vertex=2)
    # g.set_edge(from_vertex=5, to_vertex=6)
    # g.set_edge(from_vertex=6, to_vertex=3)
    # print(graph_bfs(graph=g, start_vertex=5).to_list())
    # print(graph_dfs(graph=g, start_vertex=5).to_list())
    # print(len(g), g.size())
    # print(g.get_weight(from_vertex=1, to_vertex=2))
    print("-------拓扑排序-------")
    g: Graph[int] = Graph[int]()
    g.add_vertex(vertex=1)
    g.add_vertex(vertex=2)
    g.add_vertex(vertex=3)
    g.add_vertex(vertex=4)
    g.add_vertex(vertex=5)
    g.set_edge(from_vertex=1, to_vertex=2)
    g.set_edge(from_vertex=1, to_vertex=4)
    g.set_edge(from_vertex=2, to_vertex=3)
    g.set_edge(from_vertex=2, to_vertex=4)
    g.set_edge(from_vertex=3, to_vertex=5)
    # g.set_edge(from_vertex=3, to_vertex=1)
    g.set_edge(from_vertex=4, to_vertex=3)
    g.set_edge(from_vertex=4, to_vertex=5)
    print(topological_sorting(graph=g).to_list())
    print(len(g), g.size())
    print("-------迪杰斯特拉算法-------")
    g2: Graph[int] = Graph[int]()
    g2.add_vertex(vertex=0)
    g2.add_vertex(vertex=1)
    g2.add_vertex(vertex=2)
    g2.add_vertex(vertex=3)
    g2.add_vertex(vertex=4)
    g2.add_vertex(vertex=5)
    g2.add_vertex(vertex=6)
    g2.add_vertex(vertex=7)
    g2.set_edge(from_vertex=0, to_vertex=1, weight=2)
    g2.set_edge(from_vertex=0, to_vertex=2, weight=9)
    g2.set_edge(from_vertex=1, to_vertex=0, weight=2)
    g2.set_edge(from_vertex=1, to_vertex=3, weight=4)
    g2.set_edge(from_vertex=1, to_vertex=4, weight=8)
    g2.set_edge(from_vertex=2, to_vertex=0, weight=9)
    g2.set_edge(from_vertex=2, to_vertex=4, weight=10)
    g2.set_edge(from_vertex=2, to_vertex=5, weight=3)
    g2.set_edge(from_vertex=3, to_vertex=1, weight=4)
    g2.set_edge(from_vertex=3, to_vertex=4, weight=1)
    g2.set_edge(from_vertex=3, to_vertex=6, weight=5)
    g2.set_edge(from_vertex=4, to_vertex=1, weight=8)
    g2.set_edge(from_vertex=4, to_vertex=2, weight=10)
    g2.set_edge(from_vertex=4, to_vertex=3, weight=1)
    g2.set_edge(from_vertex=4, to_vertex=5, weight=11)
    g2.set_edge(from_vertex=4, to_vertex=6, weight=6)
    g2.set_edge(from_vertex=4, to_vertex=7, weight=12)
    g2.set_edge(from_vertex=5, to_vertex=2, weight=3)
    g2.set_edge(from_vertex=5, to_vertex=4, weight=11)
    g2.set_edge(from_vertex=5, to_vertex=7, weight=17)
    g2.set_edge(from_vertex=6, to_vertex=3, weight=5)
    g2.set_edge(from_vertex=6, to_vertex=4, weight=6)
    g2.set_edge(from_vertex=7, to_vertex=4, weight=12)
    g2.set_edge(from_vertex=7, to_vertex=5, weight=17)
    dis: HashMap[int, int]; path: HashMap[int, LinkedList[int]]
    dis, path = dijkstra(graph=g2, start_vertex=4)
    i: int
    for i in range(8):
        print(f"起点：4，终点：{i}，最短距离：{dis[i]}, 最短路径：{path[i].to_list()}")
    print("-------图权矩阵-------")
    print(weight_matrix(graph=g2))
    print("-------弗洛伊德算法-------")
    dis2: List[Tuple[Tuple[int, int], int, LinkedList[int]]] = floyd(graph=g2)
    j: Tuple[Tuple[int, int], int, LinkedList[int]]
    for j in dis2:
        print(f"起点：{j[0][0]}，终点：{j[0][1]}，最短距离：{j[1]}，最短路径：{j[2].to_list()}")
    print("-------普里姆算法-------")
    g3: Graph[int] = prim(graph=g2)
    k: int
    for k in g3.vertexes: # type: ignore
        to_edges: HashMap[int, int] = g3[k].get_to_edges()
        k2: int
        for k2 in to_edges: # type: ignore
            print(k, k2, to_edges[k2])
    print("-------克鲁斯卡尔算法-------")
    g4: Graph[int] = kruskal(graph=g2)
    l: int
    for l in g4.vertexes: # type: ignore
        to_edges2: HashMap[int, int] = g4[l].get_to_edges()
        l2: int
        for l2 in to_edges2: # type: ignore
            print(l, l2, to_edges2[l2])