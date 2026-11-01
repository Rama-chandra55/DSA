class Solution:
    def minMoves(self, nums: list[int]) -> int:
        min_val = min(nums)
        return sum(num - min_val for num in nums)
