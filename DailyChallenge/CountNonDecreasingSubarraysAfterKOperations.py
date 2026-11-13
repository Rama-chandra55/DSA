from collections import deque
from typing import List


class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        dq = deque()
        j = len(nums) - 1
        ans = cost = 0
        for i in range(len(nums) - 1, -1, -1):
            while dq and nums[dq[-1]] < nums[i]:
                left = dq.pop()
                right = dq[-1] if dq else j + 1
                cost += (right - left) * (nums[i] - nums[left])
            dq.append(i)
            while cost > k:
                cost -= nums[dq[0]] - nums[j]
                if dq[0] == j:
                    dq.popleft()
                j -= 1
            ans += j - i + 1
        return ans
