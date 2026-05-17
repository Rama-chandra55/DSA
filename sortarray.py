from typing import List
class Solution:
    def sortArray(self, nums: List[int]) -> List[int]:
        nums.sort()
        return nums
        # n = len(nums)-1
        # for i in range(n):
        #     swapped = False
        #     for j in range(0,n):
        #         if nums[j] > nums[j+1]:
        #             nums[j],nums[j+1] = nums[j+1],nums[j]
        #             swapped = True
        #     if not swapped:
        #         break       
        # return nums               
        
