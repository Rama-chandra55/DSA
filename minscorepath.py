class Solution(object):
    def minScore(self, n, roads):
        graph = [[] for _ in range(n + 1)]

        for u, v, d in roads:
            graph[u].append((v, d))
            graph[v].append((u, d))

        visited = [False] * (n + 1)
        ans = float('inf')

        stack = [1]
        visited[1] = True

        while stack:
            node = stack.pop()

            for nei, dist in graph[node]:
                ans = min(ans, dist)
                if not visited[nei]:
                    visited[nei] = True
                    stack.append(nei)

        return ans
