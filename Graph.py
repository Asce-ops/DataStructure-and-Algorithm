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
from sys import maxsize
from LinkedList import LinkedList
from copy import deepcopy


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



def dijkstra(graph: Graph, start_vertex: int) -> tuple[HashMap, HashMap]:
    '''Dijkstra 算法确定非负加权图的单源最短路径'''
    unvisited_vertexs: HashMap = HashMap()
    for vertex in graph.vertexs:
        '''初始化所有节点距离为无穷大'''
        unvisited_vertexs[vertex] = maxsize
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



def prim(graph: Graph) -> Graph:
    '''prim 算法最小生成树'''
    selected: HashMap = HashMap() # 模拟集合，{vertex}
    first_vertex: int = next(iter(graph.vertexs))
    selected.put(key=first_vertex, val=None) # 从第一个顶点开始
    unselected: list[int] = graph.vertexs.keys()
    unselected.remove(first_vertex)
    used_edges: LinkedList = LinkedList() # 用于组成最小生成树的边
    while len(unselected) > 0:
        minimum: int = maxsize
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
    return minimum_spanning_tree



def topological_sorting(graph: Graph) -> LinkedList:
    '''
    拓扑排序是一个有向无环图的所有顶点的线性序列，并满足以下两个条件：
    1. 每个顶点出现且只出现一次。
    2. 若存在一条从顶点 A 到顶点 B 的路径，那么在序列中顶点 A 出现在顶点 B 的前面。
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
    g2.add_vertex(vertex=1)
    g2.add_vertex(vertex=2)
    g2.add_vertex(vertex=3)
    g2.add_vertex(vertex=4)
    g2.add_vertex(vertex=5)
    g2.add_vertex(vertex=6)
    g2.add_vertex(vertex=7)
    g2.add_vertex(vertex=8)
    g2.set_edge(from_vertex=1, to_vertex=2, weight=2)
    g2.set_edge(from_vertex=1, to_vertex=3, weight=9)
    g2.set_edge(from_vertex=2, to_vertex=1, weight=2)
    g2.set_edge(from_vertex=2, to_vertex=4, weight=4)
    g2.set_edge(from_vertex=2, to_vertex=5, weight=8)
    g2.set_edge(from_vertex=3, to_vertex=1, weight=9)
    g2.set_edge(from_vertex=3, to_vertex=5, weight=10)
    g2.set_edge(from_vertex=3, to_vertex=6, weight=3)
    g2.set_edge(from_vertex=4, to_vertex=2, weight=4)
    g2.set_edge(from_vertex=4, to_vertex=5, weight=1)
    g2.set_edge(from_vertex=4, to_vertex=7, weight=5)
    g2.set_edge(from_vertex=5, to_vertex=2, weight=8)
    g2.set_edge(from_vertex=5, to_vertex=3, weight=10)
    g2.set_edge(from_vertex=5, to_vertex=4, weight=1)
    g2.set_edge(from_vertex=5, to_vertex=6, weight=11)
    g2.set_edge(from_vertex=5, to_vertex=7, weight=6)
    g2.set_edge(from_vertex=5, to_vertex=8, weight=12)
    g2.set_edge(from_vertex=6, to_vertex=3, weight=3)
    g2.set_edge(from_vertex=6, to_vertex=5, weight=11)
    g2.set_edge(from_vertex=6, to_vertex=8, weight=17)
    g2.set_edge(from_vertex=7, to_vertex=4, weight=5)
    g2.set_edge(from_vertex=7, to_vertex=5, weight=6)
    g2.set_edge(from_vertex=8, to_vertex=5, weight=12)
    g2.set_edge(from_vertex=8, to_vertex=6, weight=17)
    dis, path = dijkstra(g2, start_vertex=4)
    for i in range(1, 9):
        print(i, dis[i], path[i].to_list())
    print('-------普里姆算法-------')
    g3: Graph = prim(graph=g2)
    for i in g3.vertexs:
        to_edges: HashMap = g3[i].get_to_edges()
        for j in to_edges:
            print(i, j, to_edges[j])