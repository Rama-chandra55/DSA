from collections import deque
def bfs(graph, start):
    visited = set([start])
    q = deque([start])
    while q:
        node = q.popleft()
        print(node, end=" ")
        for n in graph[node]:
            if n not in visited:
                visited.add(n)
                q.append(n)
graph = {0:[1,2], 1:[0,3], 2:[0], 3:[1]}
bfs(graph, 0)
