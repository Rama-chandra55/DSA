from functools import cache
class Solution:
    def stoneGameII(self, piles: List[int]) -> int:
        P = piles
        N = len(P)
        S = [0] * (N + 1)
        for i in range(N - 1, -1, -1):
            S[i] = S[i + 1] + P[i]

        @cache
        def dp(i, m):
            if i + 2 * m >= N: 
                return S[i]
            return S[i] - min(dp(i + x, max(m, x)) for x in range(1, 2 * m + 1))

        return dp(0, 1)
