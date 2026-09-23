class Solution:
    def minOperations(self, nums: list[int], x: int) -> int:
        t = sum(nums) - x
        if t < 0: return -1
        if t == 0: return len(nums)
        
        mx, s, l = -1, 0, 0
        for r, v in enumerate(nums):
            s += v
            while s > t:
                s -= nums[l]
                l += 1
            if s == t:
                mx = max(mx, r - l + 1)
                
        return len(nums) - mx if mx != -1 else -1
