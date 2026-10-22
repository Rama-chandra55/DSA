class Solution:
    def minOperations(self, nums: list[int]) -> int:
        n, z = len(nums), nums.index(0)
        inc = all(nums[(z + i - 1) % n] < nums[(z + i) % n] for i in range(1, n))
        dec = all(nums[(z - i + 1) % n] < nums[(z - i) % n] for i in range(1, n))
        return min([z, n - z + 2] * inc + [z + 2, n - z] * dec, default=-1)
