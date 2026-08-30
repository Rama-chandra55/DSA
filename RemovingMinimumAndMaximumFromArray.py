class Solution(object):
    def minimumDeletions(self, nums):
        n = len(nums)
        if n <= 2:
            return n
        
        # Step 1: Find the indices of the minimum and maximum elements
        min_idx = nums.index(min(nums))
        max_idx = nums.index(max(nums))
        
        # Step 2: Order indices so i is always the smaller index
        i, j = min(min_idx, max_idx), max(min_idx, max_idx)
        
        # Step 3: Calculate the 3 possible deletion strategies
        del_both_front = j + 1
        del_both_back = n - i
        del_from_both_ends = (i + 1) + (n - j)
        
        # Step 4: Return the minimum of the 3 strategies
        return min(del_both_front, del_both_back, del_from_both_ends)



        
