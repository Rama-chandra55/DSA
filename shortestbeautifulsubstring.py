class Solution(object):
    def shortestBeautifulSubstring(self, s, k):
        if s.count('1') < k:
            return ""
            
        ans = ""
        min_len = len(s) + 1
        left = 0
        ones_count = 0
        
        # Expand the window using the right pointer
        for right in range(len(s)):
            if s[right] == '1':
                ones_count += 1
                
            # Shrink the window from the left as long as it contains exactly k '1's
            while ones_count == k:
                # Calculate the length of the current beautiful substring
                curr_len = right - left + 1
                curr_str = s[left:right+1]
                
                # Update ans if a shorter window is found
                if curr_len < min_len:
                    min_len = curr_len
                    ans = curr_str
                # If lengths are equal, pick the lexicographically smaller one
                elif curr_len == min_len:
                    if curr_str < ans:
                        ans = curr_str
                
                # Move left pointer to shrink the window
                if s[left] == '1':
                    ones_count -= 1
                left += 1
                
        return ans


        


        
