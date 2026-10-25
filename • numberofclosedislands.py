class Solution:
    def closedIsland(self, grid: list[list[int]]) -> int:
        rows, cols = len(grid), len(grid[0])
        
        def dfs(r, c):
            if r < 0 or r >= rows or c < 0 or c >= cols:
                return False
            if grid[r][c] == 1:
                return True
            
            grid[r][c] = 1  # Mark as visited by turning land into water
            
            # Check all 4 directions
            down = dfs(r + 1, c)
            up = dfs(r - 1, c)
            right = dfs(r, c + 1)
            left = dfs(r, c - 1)
            
            return down and up and right and left

        closed_islands = 0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 0:
                    if dfs(r, c):
                        closed_islands += 1
                        
        return closed_islands
