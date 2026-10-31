class Solution:
    def uniquePaths(self, g: list[list[int]]) -> int:
        M = 10**9 + 7
        m, n = len(g), len(g[0])
        R = [[0] * n for _ in range(m)]
        D = [[0] * n for _ in range(m)]
        
        for r in reversed(range(m)):
            for c in reversed(range(n)):
                if g[r][c] == 1:
                    R[r][c] = D[r + 1][c] if r + 1 < m else 0
                    D[r][c] = R[r][c + 1] if c + 1 < n else 0
                else:
                    if r == m - 1 and c == n - 1:
                        R[r][c] = D[r][c] = 1
                    else:
                        v = ((R[r][c + 1] if c + 1 < n else 0) + 
                             (D[r + 1][c] if r + 1 < m else 0)) % M
                        R[r][c] = D[r][c] = v
                        
        return R[0][0] if g[0][0] == 0 else ((R[0][1] if n > 1 else 0) + (D[1][0] if m > 1 else 0)) % M
