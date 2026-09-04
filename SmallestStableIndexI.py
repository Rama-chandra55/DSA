class Solution:
    def firstStableIndex(self, nums: list[int], k: int) -> int:
        n = len(nums)
        
        # Step 1: Precompute the Suffix Minimums
        # suffix_min[i] will store the minimum value from index i to n-1
        suffix_min = [0] * n
        current_min = float('inf')
        
        for i in range(n - 1, -1, -1):
            if nums[i] < current_min:
                current_min = nums[i]
            suffix_min[i] = current_min
            
        # Step 2: Iterate from left to right tracking the Prefix Maximum
        current_max = float('-inf')
        for i in range(n):
            if nums[i] > current_max:
                current_max = nums[i]
                
            # Calculate the instability score for the current index i
            instability_score = current_max - suffix_min[i]
            
            # Return the first (smallest) index that meets the stability criteria
            if instability_score <= k:
                return i
                
        # If no stable index is found, return -1
        return -1
