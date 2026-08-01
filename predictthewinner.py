class Solution:
    def predictTheWinner(self, nums: list[int]) -> bool:
        n = len(nums)
        # dp[i][j] stores the maximum relative score the current player can get from nums[i...j]
        dp = [[0] * n for _ in range(n)]
        
        # Base case: when there is only 1 element left, the player must take it
        for i in range(n):
            dp[i][i] = nums[i]
            
        # Build the table for sub-arrays of increasing lengths
        for length in range(2, n + 1): # sub-array length
            for i in range(n - length + 1):
                j = i + length - 1
                # Option 1: Take the first element nums[i]
                # Option 2: Take the last element nums[j]
                dp[i][j] = max(nums[i] - dp[i + 1][j], nums[j] - dp[i][j - 1])
                
        # If Player 1's relative score is 0 or more, Player 1 wins
        return dp[0][n - 1] >= 0
