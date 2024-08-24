from HashMap import HashMapOpenAddressing

class Vertex:
    '''顶点'''
    def __init__(self, val: int) -> None:
        self.val: int = val # 顶点的唯一标识
        self.from_edges: HashMapOpenAddressing = HashMapOpenAddressing() # 入边，{顶点的唯一标识：权重}
        self.to_edges: HashMapOpenAddressing = HashMapOpenAddressing() # 出边，{顶点的唯一标识：权重}
        self.from_degree: int = 0 # 入度
        self.to_degree: int = 0 # 出度

    def get_from_degree(self) -> int:
        return self.from_degree
    
    def get_to_degree(self) -> int:
        return self.to_degree
    
    def get_from_edges(self) -> HashMapOpenAddressing:
        return self.from_edges
    
    def get_to_edges(self) -> HashMapOpenAddressing:
        return self.to_edges



class Graph:
    '''图'''
    def __init__(self) -> None:
        self.vertexs: HashMapOpenAddressing = HashMapOpenAddressing() # {顶点的唯一标识：顶点}
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

def graph_bfs(graph: Graph, start_vertex: int) -> DynamicArray:
    '''广度优先遍历'''
    if start_vertex not in graph:
        raise ValueError(f'顶点{start_vertex}在图中不存在')
    result: DynamicArray[int | None] = DynamicArray(capacity=len(graph)) # 避免触发数组扩容
    visited: HashMapOpenAddressing = HashMapOpenAddressing() # 用哈希表来实现集合
    queue: ArrayQueue = ArrayQueue(capacity=len(graph))
    queue.enqueue(item=graph[start_vertex])
    visited.put(key=start_vertex, val=None) # 需要在入队时添加，如果在出队时添加可能导致顶点重复入队
    while len(queue) > 0:
        cur = queue.dequeue()
        result.append(item=cur.val)
        for i in cur.get_to_edges().keys():
            if i not in visited:
                queue.enqueue(item=graph[i])
                visited.put(key=i, val=None)
    return result

def graph_dfs(graph: Graph, start_vertex: int) -> DynamicArray:
    '''深度优先遍历'''
    if start_vertex not in graph:
        raise ValueError(f'顶点{start_vertex}在图中不存在')
    result: DynamicArray[int | None] = DynamicArray(capacity=len(graph)) # 避免触发数组扩容
    visited: HashMapOpenAddressing = HashMapOpenAddressing() # 用哈希表来实现集合
    def dfs(vertex: int) -> None:
        result.append(item=vertex)
        visited.put(key=vertex, val=None)
        for i in graph[vertex].get_to_edges().keys():
            if i not in visited:
                dfs(vertex=i)
    dfs(vertex=start_vertex)
    return result



def dijkstra(graph: Graph, start_vertex: int):
    '''Dijkstra 算法确定最短路径'''
    pass



if __name__ == '__main__':
    g = Graph()
    g.add_vertex(vertex=1)
    g.add_vertex(vertex=2)
    g.add_vertex(vertex=3)
    g.set_edge(from_vertex=1, to_vertex=2)
    g.set_edge(from_vertex=1, to_vertex=4)
    g.set_edge(from_vertex=2, to_vertex=4)
    g.set_edge(from_vertex=2, to_vertex=3)
    g.set_edge(from_vertex=4, to_vertex=5)
    g.set_edge(from_vertex=5, to_vertex=2)
    g.set_edge(from_vertex=5, to_vertex=6)
    g.set_edge(from_vertex=6, to_vertex=3)
    print(graph_bfs(graph=g, start_vertex=5).to_list())
    print(graph_dfs(graph=g, start_vertex=5).to_list())
    print(len(g), g.size())
    print(g.get_weight(from_vertex=1, to_vertex=2))