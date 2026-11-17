class Solution:
    def minimumChanges(self, s: str, k: int) -> int:
        n = len(s)
        divs = {L: [d for d in range(1, L) if L % d == 0] for L in range(2, n + 1)}
        
        cost = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                L = j - i + 1
                sub_cost = float('inf')
                for d in divs[L]:
                    cnt = 0
                    m = L // d
                    for r in range(d):
                        left, right = i + r, i + r + (m - 1) * d
                        while left < right:
                            cnt += s[left] != s[right]
                            left += d
                            right -= d
                    sub_cost = min(sub_cost, cnt)
                cost[i][j] = sub_cost

        dp = [0] + [float('inf')] * n
        for part in range(1, k + 1):
            dp = [
                float('inf') if j < 2 * part else min(
                    dp[i] + cost[i][j - 1] for i in range(2 * (part - 1), j - 1)
                )
                for j in range(n + 1)
            ]
        return dp[n]
