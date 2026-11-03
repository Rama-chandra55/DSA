class Solution:
    def minMoves(self, nums: List[int]) -> int:
        big = max(nums)
        res = 0
        i = 0
        while i < len(nums):
            res += big - nums[i]
            i += 1
        return res
