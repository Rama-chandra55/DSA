from fractions import gcd

class Solution(object):
    def subsequencePairCount(self, nums):
        MOD, n = 10**9 + 7, len(nums)
        memo = {}
        
        def dfs(i, g1, g2):
            # Create a unique key for the current state
            state = (i, g1, g2)
            if state in memo:
                return memo[state]
                
            if i == n: 
                return 1 if g1 == g2 > 0 else 0
            
            x = nums[i]
            skip = dfs(i + 1, g1, g2)
            p1 = dfs(i + 1, x if not g1 else gcd(g1, x), g2)
            p2 = dfs(i + 1, g1, x if not g2 else gcd(g2, x))
            
            memo[state] = (skip + p1 + p2) % MOD
            return memo[state]
            
        return dfs(0, 0, 0)

