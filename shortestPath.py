from collections import deque
def bfs(graph, start):
    visited = set([start])
    queue = deque([start])
    while queue:
        node = queue.popleft()
        print(node, end=" ")

        for n in graph[node]:
            if n not in visited:
                visited.add(n)
                queue.append(n)
graph = {
    0: [1, 2],
    1: [0, 3, 4],
    2: [0],
    3: [1],
    4: [1]
}
bfs(graph, 0)

# Another approach - too simple
from collections import deque
def bfs(graph, start):
    visited = set([start])
    queue = deque([(start, 0)])
    while queue:
        node, d = queue.popleft()
        print(node, d)
        for n in graph[node]:
            if n not in visited:
                visited.add(n)
                queue.append((n, d+1))

