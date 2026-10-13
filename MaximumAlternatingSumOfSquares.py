class Solution:
    def maxAlternatingSum(self, nums: List[int]) -> int:
        squares = sorted(x * x for x in nums)
        k = len(nums) // 2
        return sum(squares[k:]) - sum(squares[:k])
