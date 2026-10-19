class Solution:
    def targetIndices(self, nums: list[int], target: int) -> list[int]:
        num = sorted(nums)
        res = []
        for i in range(len(num)):
            if num[i] == target:
                res.append(i)
        return res
