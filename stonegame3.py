class Solution:
    def stoneGameIII(self, stoneValue: List[int]) -> str:
        n = len(stoneValue)

        dp = [0] * (n + 1)

        for i in range(n - 1, -1, -1):
            max_score = float('-inf')
            take = 0

            for k in range(3):
                if i + k < n:
                    take += stoneValue[i + k]
        
                    max_score = max(max_score, take - dp[i + k + 1])
            
            dp[i] = max_score

        if dp[0] > 0:
            return "Alice"
        elif dp[0] < 0:
            return "Bob"
        else:
            return "Tie"

            
