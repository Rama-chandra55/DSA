import math

class Solution:
    def maxLength(self, nums: list[int]) -> int:
        ans = 0
        n = len(nums)
        for i in range(n):
            p, g, l = 1, 0, 1
            for j in range(i, n):
                x = nums[j]
                p *= x
                g = math.gcd(g, x)
                l = (l * x) // math.gcd(l, x)
                if p == l * g:
                    ans = max(ans, j - i + 1)
        return ans
