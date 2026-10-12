class Solution:
    def maxSum(self, nums: list[int], k: int) -> int:
        MOD = 1_000_000_007
        bits = [0] * 30
        
        for n in nums:
            for i in range(30):
                bits[i] += (n >> i) & 1
                    
        ans = 0
        for _ in range(k):
            val = 0
            for i in range(30):
                if bits[i]:
                    val |= (1 << i)
                    bits[i] -= 1
            ans = (ans + val * val) % MOD
            
        return ans
