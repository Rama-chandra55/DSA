from collections import deque

class Solution:
    def findSafeWalk(self, grid: list[list[int]], health: int) -> bool:
        m, n = len(grid), len(grid[0])

        min_cost = [[float('inf')] * n for _ in range(m)]

        queue = deque()
  
        start_cost = grid[0][0]
        min_cost[0][0] = start_cost
        queue.append((0, 0, start_cost))

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        while queue:
            r, c, current_cost = queue.popleft()

            if current_cost >= health:
                continue

            for dr, dc in directions:
                nr, nc = r + dr, c + dc

                if 0 <= nr < m and 0 <= nc < n:
                    next_cost = current_cost + grid[nr][nc]

                    if next_cost < min_cost[nr][nc]:
                        min_cost[nr][nc] = next_cost

                        if grid[nr][nc] == 0:
                            queue.appendleft((nr, nc, next_cost))
                        else:
                            queue.append((nr, nc, next_cost))

        return health - min_cost[m - 1][n - 1] >= 1
