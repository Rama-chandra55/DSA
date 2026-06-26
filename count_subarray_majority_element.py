class Solution(object):
    def countMajoritySubarrays(self, nums, target):
        n = len(nums)
        offset = n
        counts = [0] * (2 * n + 1)

        running_sum = 0
        counts[running_sum + offset] = 1
        
        valid_prev_prefixes = 0
        total_subarrays = 0
        
        for num in nums:
            if num == target:

                valid_prev_prefixes += counts[running_sum + offset]
                running_sum += 1
            else:
   
                running_sum -= 1

                valid_prev_prefixes -= counts[running_sum + offset]

            total_subarrays += valid_prev_prefixes
            
            counts[running_sum + offset] += 1
            
        return total_subarrays
