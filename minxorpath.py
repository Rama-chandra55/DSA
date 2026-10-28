class Solution:
    def minCost(self, G: list[list[int]]) -> int:
        R, C = len(G), len(G[0])
        dp = [[set() for _ in range(C)] for _ in range(R)]
        dp[0][0].add(G[0][0])
        
        for r in range(R):
            for c in range(C):
                for v in dp[r][c]:
                    if r + 1 < R: dp[r + 1][c].add(v ^ G[r + 1][c])
                    if c + 1 < C: dp[r][c + 1].add(v ^ G[r][c + 1])
                    
        return min(dp[-1][-1])
