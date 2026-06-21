class Solution(object):
    def minPairSum(self, nums):
        nums.sort() 
        
        max_sum = 0
        n = len(nums)
        for i in range(n // 2):

            pair_sum = nums[i] + nums[n - 1 - i]
             
            if pair_sum > max_sum:
                max_sum = pair_sum
                
        return max_sum
        
