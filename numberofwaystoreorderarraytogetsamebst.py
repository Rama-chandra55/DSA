import math
from typing import List

class Solution:
    def numOfWays(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        
        def dfs(arr: List[int]) -> int:
            if len(arr) <= 2:
                return 1
            
            root = arr[0]
            l = [x for x in arr[1:] if x < root]
            r = [x for x in arr[1:] if x > root]
            
            ways = math.comb(len(l) + len(r), len(l))
            return (ways * dfs(l) * dfs(r)) % MOD

        return (dfs(nums) - 1) % MOD
