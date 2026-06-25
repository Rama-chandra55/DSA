class Solution(object):
    def countMajoritySubarrays(self, nums, target):
        n = len(nums)
        ans = 0

        for i in range(n):
            count_target = 0

            for j in range(i, n):
                if nums[j] == target:
                    count_target += 1

                length = j - i + 1

                if 2 * count_target > length:
                    ans += 1

        return ans
