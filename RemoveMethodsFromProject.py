class Solution:
    def remainingMethods(self, n: int, k: int, invocations: list[list[int]]) -> list[int]:
        # Build adjacency list for directed graph
        graph = [[] for _ in range(n)]
        for u, v in invocations:
            graph[u].append(v)
            
        # Step 1: Identify all suspicious methods reachable from k
        suspicious = [False] * n
        def dfs(node):
            suspicious[node] = True
            for neighbor in graph[node]:
                if not suspicious[neighbor]:
                    dfs(neighbor)
        dfs(k)
        
        # Step 2: Check if any non-suspicious method invokes a suspicious method
        for u, v in invocations:
            if not suspicious[u] and suspicious[v]:
                # External dependency found; cannot remove any method
                return list(range(n))
                
        # Step 3: Return all non-suspicious methods
        return [i for i in range(n) if not suspicious[i]]
