from typing import List
from collections import deque

class Solution:
    def findMaxPathScore(self, edges: List[List[int]], online: List[bool], k: int) -> int:
        n = len(online)

        graph = [[] for _ in range(n)]
        indegree = [0] * n
        costs = []

        for u, v, c in edges:
            graph[u].append((v, c))
            indegree[v] += 1
            costs.append(c)

        q = deque(i for i in range(n) if indegree[i] == 0)
        topo = []

        while q:
            u = q.popleft()
            topo.append(u)
            for v, _ in graph[u]:
                indegree[v] -= 1
                if indegree[v] == 0:
                    q.append(v)

        INF = 10**30

        def check(limit):
            dist = [INF] * n
            dist[0] = 0

            for u in topo:
                if dist[u] == INF:
                    continue
                if u != 0 and u != n - 1 and not online[u]:
                    continue

                for v, c in graph[u]:
                    if c < limit:
                        continue
                    if v != 0 and v != n - 1 and not online[v]:
                        continue
                    if dist[u] + c < dist[v]:
                        dist[v] = dist[u] + c

            return dist[n - 1] <= k

        if not check(0):
            return -1

        left, right = 0, max(costs, default=0)
        ans = 0

        while left <= right:
            mid = (left + right) // 2
            if check(mid):
                ans = mid
                left = mid + 1
            else:
                right = mid - 1

        return ans
