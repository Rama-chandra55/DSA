class Solution:
    def minimumPositiveSumSubarray(self, nums: list[int], l: int, r: int) -> int:
        n = len(nums)
        pref = [0] * (n + 1)
        for i, x in enumerate(nums):
            pref[i + 1] = pref[i] + x

        ans = float("inf")
        for size in range(l, r + 1):
            for i in range(n - size + 1):
                s = pref[i + size] - pref[i]
                if 0 < s < ans:
                    ans = s

        return ans if ans != float("inf") else -1
