class Solution:
    def minSumOfLengths(self, arr: list[int], target: int) -> int:
        seen = {0: -1}

        min_len = [float('inf')] * len(arr)
        
        current_sum = 0
        min_so_far = float('inf')
        result = float('inf')
        
        for i, num in enumerate(arr):
            current_sum += num
            seen[current_sum] = i
            
          needed_sum = current_sum - target
            if needed_sum in seen:
                start_idx = seen[needed_sum]
                current_len = i - start_idx
                
              if start_idx >= 0 and min_len[start_idx] != float('inf'):
                    result = min(result, current_len + min_len[start_idx])
                
                min_so_far = min(min_so_far, current_len)
            
            min_len[i] = min_so_far
            
        return result if result != float('inf') else -1
