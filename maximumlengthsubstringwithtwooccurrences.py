class Solution(object):
    def maximumLengthSubstring(self, s):
        counts = {}
        
        max_len = 0
        left = 0
        
        # Expand the window using the right pointer
        for right in range(len(s)):
            char_right = s[right]
            counts[char_right] = counts.get(char_right, 0) + 1
            
            # Shrink the window from the left if any character count exceeds 2
            while counts[char_right] > 2:
                char_left = s[left]
                counts[char_left] -= 1
                left += 1
                
            # Calculate the current valid window size
            current_len = right - left + 1
            if current_len > max_len:
                max_len = current_len
                
        return max_len
        
