import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent)) # Path(__file__) 获取的当前 py 文件的路径

from Array import DynamicArray
from Graph import Graph, graph_dfs



def knight_graph(rows: int, cols: int) -> Graph:
    '''
    构建骑士周游图
    棋盘左下角为0，右上角为 rows * cols - 1
    '''
    graph: Graph = Graph()
    def legal_moves(row: int, col: int) -> DynamicArray:
        '''生成骑士在当前位置合法的走法'''
        next_moves: DynamicArray = DynamicArray(capacity=8)
        move_offsets: list[tuple[int, int]] = [(-1, -2), (-1, 2), (-2, -1), (-2, 1), (1, -2), (1, 2), (2, -1), (2, 1)]
        for row_off, col_off in move_offsets:
            next_row: int = row + row_off
            next_col: int = col + col_off
            if (0 <= next_row < rows) and (0 <= next_col < cols): # 合法的走法需仍在棋盘内
                next_moves.append(item=next_row * cols + next_col)
        return next_moves
    for row in range(rows):
        for col in range(cols):
            cur: int = row * cols + col
            graph.add_vertex(vertex=cur)
            next_moves: DynamicArray[int] = legal_moves(row=row, col=col)
            for next_move in next_moves:
                graph.set_edge(from_vertex=cur, to_vertex=next_move)
    return graph



def knight_tour(graph: Graph, start_vertex: int) -> DynamicArray:
    '''生成骑士周游的路径'''
    return graph_dfs(graph=graph, start_vertex=start_vertex)



if __name__ == '__main__':
    g: Graph = knight_graph(rows=8, cols=8)
    print(knight_tour(graph=g, start_vertex=0).to_list())