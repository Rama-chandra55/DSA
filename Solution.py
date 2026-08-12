class Solution:
    def maxSubarrayLength(self, nums: List[int], k: int) -> int:
        freq={}
        l=max_len=0
        for r in range(len(nums)):
            freq[nums[r]] = freq.get(nums[r],0) + 1
            while freq[nums[r]] > k:
                freq[nums[l]] -= 1
                l += 1
            max_len = max(max_len, r-l+1)
        return max_len
