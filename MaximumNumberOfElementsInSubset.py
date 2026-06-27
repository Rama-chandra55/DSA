from collections import Counter
import math
class Solution(object):
    def maximumLength(self, nums):
        count = Counter(nums)
        max_len = 1

        if 1 in count:
            ones_count = count[1]
            if ones_count % 2 == 0:
                max_len = max(max_len, ones_count - 1)
            else:
                max_len = max(max_len, ones_count)
        for num in count:
            if num == 1:
                continue
                
            current_len = 0
            current = num
     
            while current in count and count[current] >= 2:
                current_len += 2
                current = current * current
            if current in count:
                current_len += 1
            else:
                current_len -= 1
                
            max_len = max(max_len, current_len)
            
        return max_len
        
