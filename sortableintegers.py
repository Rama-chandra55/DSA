import math

class Solution:
    def sumOfSortableIntegers(self, nums: list[int]) -> int:
        n = len(nums)
        p_dp = [0] * n
        for i in range(1, n):
            p_dp[i] = p_dp[i-1] + (nums[i-1] > nums[i])
            
        p_mx = [0] * n
        p_mx[0] = nums[0]
        for i in range(1, n):
            p_mx[i] = max(p_mx[i-1], nums[i])
            
        s_mn = [0] * n
        s_mn[-1] = nums[-1]
        for i in range(n - 2, -1, -1):
            s_mn[i] = min(s_mn[i+1], nums[i])
            
        def check(k: int) -> bool:
            if any(p_mx[b-1] > s_mn[b] for b in range(k, n, k)):
                return False
            for s in range(0, n, k):
                e = s + k - 1
                if (p_dp[e] - p_dp[s] + (nums[e] > nums[s])) > 1:
                    return False
            return True

        ans = 0
        for k in range(1, int(math.isqrt(n)) + 1):
            if n % k == 0:
                if check(k): ans += k
                if k * k != n and check(n // k): ans += n // k
        return ans
