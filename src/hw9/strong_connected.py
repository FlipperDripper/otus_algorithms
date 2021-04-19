from collections import defaultdict

# алгоритм Косарайю, рекурсивный вариант
class GraphWithKosarayru:

    def __init__(self, vertex):
        self.V = vertex
        self.graph = defaultdict(list)

    # собираем массивы смежности
    def add_edge(self, s, d):
        self.graph[s].append(d)

    # поиск в глубину
    def dfs(self, d, visited_vertex):
        visited_vertex[d] = True
        print(d, end='')
        for i in self.graph[d]:
            if not visited_vertex[i]:
                self.dfs(i, visited_vertex)

    def fill_order(self, d, visited_vertex, stack):
        visited_vertex[d] = True
        for i in self.graph[d]:
            if not visited_vertex[i]:
                self.fill_order(i, visited_vertex, stack)
        stack = stack.append(d)

    # граф с обратными (инвертированными) ребрами
    def transpose(self):
        g = GraphWithKosarayru(self.V)

        for i in self.graph:
            for j in self.graph[i]:
                g.add_edge(j, i)
        return g

    # получаем компоненты сильной связности
    def get_scc(self):
        stack = []
        visited_vertex = [False] * (self.V)

        for i in range(self.V):
            if not visited_vertex[i]:
                self.fill_order(i, visited_vertex, stack)

        gr = self.transpose()

        visited_vertex = [False] * (self.V)

        while stack:
            i = stack.pop()
            if not visited_vertex[i]:
                gr.dfs(i, visited_vertex)
                print("")

