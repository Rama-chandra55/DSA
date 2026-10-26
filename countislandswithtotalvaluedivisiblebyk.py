from typing import List

class Solution:
    def countIslands(self, grid: List[List[int]], k: int) -> int:
        m, n = len(grid), len(grid[0])
        island_count = 0
        
        def dfs(r: int, c: int) -> int:
            # Add current cell value
            current_sum = grid[r][c]
            # Mark as visited by sinking the cell to 0
            grid[r][c] = 0
            
            # Explore 4-directional neighbors
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] > 0:
                    current_sum += dfs(nr, nc)
                    
            return current_sum

        for r in range(m):
            for c in range(n):
                if grid[r][c] > 0:
                    # Calculate the total value of the current island
                    total_value = dfs(r, c)
                    # Check if the total island value is divisible by k
                    if total_value % k == 0:
                        island_count += 1
                        
        return island_count
