class Solution(object):
    def stoneGameVIII(self, stones):
        for i in range(1, len(stones)):
            stones[i] += stones[i - 1]
        dp = stones[-1]
        for i in range(len(stones) - 2, 0, -1):
            dp = max(dp, stones[i] - dp)
            
        return dp
        
