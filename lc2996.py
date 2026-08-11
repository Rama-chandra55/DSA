class Solution(object):
    def missingInteger(self, nums):
        add=0
        prefix = [nums[0]]
        for i in range(1,len(nums)):
            if nums[i] == nums[i-1] + 1:
                prefix.append(nums[i])
            else:
                break
        tot = sum(prefix)
        while tot in nums:
            tot += 1
        return tot


            
        
