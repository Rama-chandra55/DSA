from functools import cache
from typing import List

class Solution:
    def hasValidPath(self, grid: List[List[str]]) -> bool:
        m, n = len(grid), len(grid[0])

        if (m + n - 1) % 2 != 0:
            return False
            
        @cache
        def dfs(i: int, j: int, k: int) -> bool:

            if i >= m or j >= n:
                return False

            k += 1 if grid[i][j] == '(' else -1

            if k < 0:
                return False

            if i == m - 1 and j == n - 1:
                return k == 0

            return dfs(i + 1, j, k) or dfs(i, j + 1, k)
            
        return dfs(0, 0, 0)
