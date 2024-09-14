from HashMap import HashMapOpenAddressing as HashMap

class Vertex:
    '''顶点'''
    def __init__(self, val: int) -> None:
        self.val: int = val # 顶点的唯一标识
        self.from_edges: HashMap = HashMap() # 入边，{顶点的唯一标识：权重}
        self.to_edges: HashMap = HashMap() # 出边，{顶点的唯一标识：权重}
        self.from_degree: int = 0 # 入度
        self.to_degree: int = 0 # 出度

    def get_from_degree(self) -> int:
        return self.from_degree
    
    def get_to_degree(self) -> int:
        return self.to_degree
    
    def get_from_edges(self) -> HashMap:
        return self.from_edges
    
    def get_to_edges(self) -> HashMap:
        return self.to_edges



class Graph:
    '''图'''
    def __init__(self) -> None:
        self.vertexs: HashMap = HashMap() # {顶点的唯一标识：顶点}
        self.vertexs_num: int = 0 # 顶点数量
        self.edges_num: int = 0 # 边的数量

    def add_vertex(self, vertex: int) -> None:
        '''添加顶点'''
        if vertex in self.vertexs:
            return
        self.vertexs[vertex] = Vertex(val=vertex)
        self.vertexs_num += 1

    def set_edge(self, from_vertex: int, to_vertex: int, weight: int = 1) -> None:
        '''添加或更新边'''
        if from_vertex not in self.vertexs: # 边所连接的顶点不存在，添加顶点
            self.add_vertex(vertex=from_vertex)
        if to_vertex not in self.vertexs:
            self.add_vertex(vertex=to_vertex)
        '''更新顶点的出入边和出入度'''
        if to_vertex not in self.vertexs[from_vertex].to_edges: # 则 from_vertex not in self.vertexs[to_vertex].from_edges
            '''边不存在'''
            self.vertexs[from_vertex].to_degree += 1
            self.vertexs[to_vertex].from_degree += 1
            self.edges_num += 1
        self.vertexs[from_vertex].to_edges[to_vertex] = weight
        self.vertexs[to_vertex].from_edges[from_vertex] = weight

    def remove_vertex(self, vertex: int) -> None:
        '''删除顶点'''
        for v in self.vertexs:
            if v == vertex: # 定位到待删除的顶点
                if v in self.vertexs[v].to_edges: # 有指向自己的边，则入边和出边中有一条重复
                    self.edges_num -= (self.vertexs[v].to_degree + self.vertexs[v].from_degree - 1)
                else:
                    self.edges_num -= (self.vertexs[v].to_degree + self.vertexs[v].from_degree)
                '''更新和待删除顶点相连的顶点的出入边和出入度'''
                for i in self.vertexs[v].to_edges:
                    del self.vertexs[i].from_edges[v]
                    self.vertexs[i].from_degree -= 1
                for i in self.vertexs[v].from_edges:
                    del self.vertexs[i].to_edges[v]
                    self.vertexs[i].to_degree -= 1
                del self.vertexs[v]
                self.vertexs_num -= 1
                return
        raise ValueError(f'顶点{vertex}在图中不存在')
    
    def remove_edge(self, from_vertex: int, to_vertex: int) -> None:
        '''删除边'''
        if (from_vertex in self.vertexs) and (to_vertex in self.vertexs):
            if to_vertex in self.vertexs[from_vertex].to_edges:
                del self.vertexs[from_vertex].to_edges[to_vertex]
                self.vertexs[from_vertex].to_degree -= 1
                del self.vertexs[to_vertex].from_edges[from_vertex]
                self.vertexs[to_vertex].from_degree -= 1
                self.edges_num -= 1
                return
        raise ValueError(f'边{from_vertex} --> {to_vertex}在图中不存在')
    
    def get(self, vertex: int) -> Vertex:
        '''查看顶点'''
        return self.vertexs[vertex]
    
    def get_weight(self, from_vertex: int, to_vertex: int) -> int:
        '''查看边的权重'''
        if from_vertex in self.vertexs:
            try:
                return self.vertexs[from_vertex].to_edges[to_vertex]
            except KeyError:
                pass
        raise ValueError(f'边{from_vertex} --> {to_vertex}在图中不存在')
    
    def __getitem__(self, vertex: int) -> Vertex:
        return self.get(vertex=vertex)
    
    def __len__(self) -> int:
        '''查看顶点的数量'''
        return self.vertexs_num
    
    def size(self) -> int:
        '''查看边的数量'''
        return self.edges_num
    
    def __contains__(self, vertex: int) -> bool:
        '''判断顶点是否在图中'''
        return vertex in self.vertexs
    


from Queue import ArrayQueue
from Array import DynamicArray
from LinkedList import LinkedList
from copy import deepcopy
from UnionFindSet import UnionFindSet
from Stack import ArrayStack



# 不重不漏地访问图中的所有顶点
def graph_bfs(graph: Graph, start_vertex: int) -> DynamicArray:
    '''广度优先遍历'''
    if start_vertex not in graph:
        raise ValueError(f'顶点{start_vertex}在图中不存在')
    result: DynamicArray[int | None] = DynamicArray(capacity=len(graph)) # 避免触发数组扩容
    visited: HashMap = HashMap() # 用哈希表来实现集合
    queue: ArrayQueue = ArrayQueue(capacity=len(graph))
    queue.enqueue(item=graph[start_vertex])
    visited.put(key=start_vertex, val=None) # 需要在入队时添加，如果在出队时添加可能导致顶点重复入队
    while len(queue) > 0:
        cur = queue.dequeue()
        result.append(item=cur.val)
        for i in cur.get_to_edges():
            if i not in visited:
                queue.enqueue(item=graph[i])
                visited.put(key=i, val=None)
    return result


def graph_dfs(graph: Graph, start_vertex: int) -> DynamicArray:
    '''深度优先遍历'''
    if start_vertex not in graph:
        raise ValueError(f'顶点{start_vertex}在图中不存在')
    result: DynamicArray[int | None] = DynamicArray(capacity=len(graph)) # 避免触发数组扩容
    visited: HashMap = HashMap() # 用哈希表来实现集合
    def dfs(vertex: int) -> None:
        result.append(item=vertex)
        visited.put(key=vertex, val=None)
        for i in graph[vertex].get_to_edges():
            if i not in visited:
                dfs(vertex=i)
    dfs(vertex=start_vertex)
    return result



# 最短路径
def dijkstra(graph: Graph, start_vertex: int) -> tuple[HashMap, HashMap]:
    '''迪杰斯特拉算法确定非负加权图的单源最短路径'''
    unvisited_vertexs: HashMap = HashMap()
    for vertex in graph.vertexs:
        '''初始化所有节点距离为无穷大'''
        unvisited_vertexs[vertex] = float('inf')
    unvisited_vertexs[start_vertex] = 0 # 起始节点距离为0
    shortest_paths: HashMap = HashMap() # {vertex: LinkedList}
    shortest_distances: HashMap = HashMap() # {vertex: int}
    shortest_paths[start_vertex], shortest_distances[start_vertex] = LinkedList(), 0
    while len(unvisited_vertexs) > 0:
        current_vertex: int = min(unvisited_vertexs, key=unvisited_vertexs.get) # 找到未访问节点中距离最近的节点
        current_distance: int = unvisited_vertexs[current_vertex]
        to_edges: HashMap = graph[current_vertex].get_to_edges()
        for neighbor in to_edges:
            if neighbor in unvisited_vertexs: # 已访问过的节点跳过
                new_distance: int = current_distance + to_edges[neighbor]
                if new_distance < unvisited_vertexs[neighbor]: # 如果找到更短路径，更新
                    unvisited_vertexs[neighbor] = new_distance
                    shortest_distances[neighbor] = new_distance
                    shortest_paths[neighbor] = deepcopy(shortest_paths[current_vertex])
                    shortest_paths[neighbor].append(neighbor)
        del unvisited_vertexs[current_vertex] # 当前节点已访问过，从未访问节点中删除
    return (shortest_distances, shortest_paths)



def weight_matrix(graph: Graph) -> list[list]:
    '''返回图的距离矩阵'''
    result: list[list] = [[float('inf')] * len(graph) for _ in range(len(graph))] # result[i][j] 为无穷表示不存在从 i 到 j 的边
    for from_vertex in graph.vertexs:
        result[from_vertex][from_vertex] = 0 # 没有自身到自身的边则设为 0
        to_edges: HashMap = graph[from_vertex].get_to_edges()
        for to_vertex in to_edges:
            result[from_vertex][to_vertex] = to_edges[to_vertex]
    return result

def floyd(graph: Graph) -> list[tuple[tuple[int, int], int, LinkedList]]:
    '''弗洛伊德算法确定非负加权图的多源最短路径'''
    n: int = len(graph)
    D: list[list] = weight_matrix(graph=graph) # D[i][j] 表示从 i 到 j 的最短距离
    P: list[list] = [[None] * n for _ in range(n)] # P[i][j] 表示从 i 到 j 的最短路径中 j 的前一个顶点
    for from_vertex in graph.vertexs:
        to_edges: HashMap = graph[from_vertex].get_to_edges()
        for to_vertex in to_edges:
            P[from_vertex][to_vertex] = from_vertex
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
    '''返回任意两点间的最短距离和对应路径'''
    result = [None] * n**2
    idx: int = 0
    for from_vertex in range(n):
        for to_vertex in range(n):
            path: LinkedList = LinkedList()
            distance: int | float = D[from_vertex][to_vertex]
            '''确定最短距离对应的路径'''
            if (distance == 0) or (distance == float('inf')):
                result[idx] = ((from_vertex, to_vertex), distance, path)
            else:
                stack: ArrayStack = ArrayStack() # 存储最短路径经过的每一个顶点
                stack.push(item=to_vertex)
                middle_vertex: int = P[from_vertex][to_vertex]
                stack.push(item=middle_vertex)
                while from_vertex != middle_vertex:
                    middle_vertex = P[from_vertex][middle_vertex]
                    stack.push(item=middle_vertex)
                while len(stack) > 0:
                    path.append(val=stack.pop())
                    result[idx] = ((from_vertex, to_vertex), distance, path)
            idx += 1
    return result



# 最小生成树：连通图（任意顶点 v 到顶点 w 之间都存在路径）中的一个子图，使得所有顶点都相互连通，且总边权和最小
def prim(graph: Graph) -> Graph:
    '''
    普里姆算法最小生成树：
    1. 首先选择一个起始节点，以这个节点将图分成两个集合。一个已选集合，一个未选集合，把起始节点加入已选集合；
    2. 从未选节点集合中选择距离已选节点集合最近的节点，并将其加入已选节点集合；
    3. 不断重复步骤 2，直到所有节点都被加入到已选节点集合中，形成最小生成树。
    '''
    selected: HashMap = HashMap() # 模拟集合，{vertex}
    first_vertex: int = next(iter(graph.vertexs))
    selected.put(key=first_vertex, val=None) # 从第一个顶点开始
    unselected: list[int] = graph.vertexs.keys()
    unselected.remove(first_vertex)
    used_edges: LinkedList = LinkedList() # 用于组成最小生成树的边
    while len(unselected) > 0:
        minimum: int = float('inf')
        from_vertex: int | None = None
        to_vertex: int | None = None
        '''从未选中部分找到距离已选中部分最近的顶点'''
        for vertex in selected:
            to_edges: HashMap = graph[vertex].get_to_edges()
            for neighbor in to_edges:
                if neighbor in unselected:
                    if to_edges[neighbor] < minimum: # 找到权值最小的边
                        minimum = to_edges[neighbor]
                        from_vertex = vertex
                        to_vertex = neighbor
        used_edges.append(val=[from_vertex, to_vertex, minimum])
        selected.put(key=to_vertex, val=None)
        unselected.remove(to_vertex)
    '''利用组成最小生成树的边构建一个子图'''
    minimum_spanning_tree: Graph = Graph()
    for edge in used_edges:
        minimum_spanning_tree.set_edge(from_vertex=edge[0], to_vertex=edge[1], weight=edge[2])
        minimum_spanning_tree.set_edge(from_vertex=edge[1], to_vertex=edge[0], weight=edge[2])
    return minimum_spanning_tree



def kruskal(graph: Graph) -> Graph:
    '''
    克鲁斯卡尔算法最小生成树：
    取出所有的边，按其权值从小到大的顺序排列，
    然后不断取出权值最小的边放入图中，一共取顶点数减 1 条边。
    但是每次放入一条边都要判断是否形成了环；
    如果没有形成环，则将该边纳入最小生成树中，
    如果形成了环，则舍弃这条边，继续取下一条边。
    '''
    used_edges: LinkedList = LinkedList() # 用于组成最小生成树的边
    ufs: UnionFindSet = UnionFindSet(arr=graph.vertexs.keys()) # 初始化并查集
    '''获取所有的边'''
    edges: list[tuple[int, int, int] | None] = [None] * graph.size()
    idx: int = 0
    for from_vertex in graph.vertexs:
        to_edges: HashMap = graph[from_vertex].get_to_edges()
        for to_vertex in to_edges:
            edges[idx] = (from_vertex, to_vertex, to_edges[to_vertex])
            idx += 1
    edges.sort(key=lambda edge: edge[2], reverse=True) # 将所有的边按照权重降序排序
    while len(used_edges) < len(graph) - 1:
        from_vertex, to_vertex, weight = edges.pop()
        if not ufs.is_relative(node1=from_vertex, node2=to_vertex): # from_vertex 和 to_vertex 是否已经连通
            ufs.union(node1=from_vertex, node2=to_vertex)
            used_edges.append(val=(from_vertex, to_vertex, weight))
    '''利用组成最小生成树的边构建一个子图'''
    minimum_spanning_tree: Graph = Graph()
    for edge in used_edges:
        minimum_spanning_tree.set_edge(from_vertex=edge[0], to_vertex=edge[1], weight=edge[2])
        minimum_spanning_tree.set_edge(from_vertex=edge[1], to_vertex=edge[0], weight=edge[2])
    return minimum_spanning_tree



def topological_sorting(graph: Graph) -> LinkedList:
    '''
    拓扑排序是一个有向无环图（环是一条只有第一个和最后一个顶点重复的非空路径）的所有顶点的线性序列，并满足以下两个条件：
    1. 每个顶点出现且只出现一次；
    2. 若存在一条从顶点 A 到顶点 B 的路径，则在序列中顶点 A 出现在顶点 B 的前面。
    '''
    graph: Graph = deepcopy(graph)
    result: LinkedList = LinkedList()
    for _ in range(len(graph)):
        for vertex in graph.vertexs:
            if graph.vertexs[vertex].from_degree == 0:
                result.append(val=vertex)
                graph.remove_vertex(vertex=vertex)
                break
        else:
            raise AttributeError('图中存在环，找不到入度为 0 的顶点')
    return result



if __name__ == '__main__':
    # g = Graph()
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
    print('-------拓扑排序-------')
    g: Graph = Graph()
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
    print('-------迪杰斯特拉算法-------')
    g2: Graph = Graph()
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
    dis, path = dijkstra(g2, start_vertex=4)
    for i in range(8):
        print(f'起点：4，终点：{i}，最短距离：{dis[i]}, 最短路径：{path[i].to_list()}')
    print('-------图权矩阵-------')
    print(weight_matrix(graph=g2))
    print('-------弗洛伊德算法-------')
    dis = floyd(graph=g2)
    for i in dis:
        print(f'起点：{i[0][0]}，终点：{i[0][1]}，最短距离：{i[1]}，最短路径：{i[2].to_list()}')
    print('-------普里姆算法-------')
    g3: Graph = prim(graph=g2)
    for i in g3.vertexs:
        to_edges: HashMap = g3[i].get_to_edges()
        for j in to_edges:
            print(i, j, to_edges[j])
    print('-------克鲁斯卡尔算法-------')
    g4: Graph = kruskal(graph=g2)
    for i in g4.vertexs:
        to_edges: HashMap = g4[i].get_to_edges()
        for j in to_edges:
            print(i, j, to_edges[j])