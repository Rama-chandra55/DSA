class Solution:
    def firstStableIndex(self, nums: list[int], k: int) -> int:
        n = len(nums)
        if n == 0:
            return -1
        
        # Step 1: Build the suffix minimum array
        suffix_min = [0] * n
        suffix_min[-1] = nums[-1]
        for i in range(n - 2, -1, -1):
            suffix_min[i] = min(nums[i], suffix_min[i + 1])
            
        # Step 2: Iterate left-to-right keeping track of prefix max
        current_max = float('-inf')
        for i in range(n):
            current_max = max(current_max, nums[i])
            
            # Step 3: Compute the instability score
            instability_score = current_max - suffix_min[i]
            
            if instability_score <= k:
                return i
                
        return -1
