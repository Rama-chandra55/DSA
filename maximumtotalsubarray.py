class Solution(object):
    def maxTotalValue(self, nums, k):
        return k * (max(nums) - min(nums))
