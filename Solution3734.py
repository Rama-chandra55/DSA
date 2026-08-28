class Solution:
    def lexPalindromicPermutation(self, s: str, target: str) -> str:
        n = len(s)

        counts = [0] * 26
        for char in s:
            counts[ord(char) - ord('a')] += 1
    
        odd_count = 0
        mid_char = ""
        half_counts = [0] * 26
        
        for i in range(26):
            if counts[i] % 2 != 0:
                odd_count += 1
                mid_char = chr(ord('a') + i)
            half_counts[i] = counts[i] // 2
            
        if odd_count > 1:
            return ""
            
        half_len = n // 2
        memo = {}
 
        def backtrack(index, is_greater):
            if index == half_len:

                left_str = "".join(current_prefix)
     
                full_pal = left_str + mid_char + left_str[::-1]
 
                if is_greater or full_pal > target:
                    return full_pal
                return ""
                
            state = (index, is_greater, tuple(half_counts))
            if state in memo:
                return memo[state]
                
            start_char_idx = 0 if is_greater else ord(target[index]) - ord('a')
            
            for i in range(start_char_idx, 26):
                if half_counts[i] > 0:
                    char = chr(ord('a') + i)
                    current_prefix.append(char)
                    half_counts[i] -= 1

                    next_greater = is_greater or (i > ord(target[index]) - ord('a'))
                    result = backtrack(index + 1, next_greater)
    
                    if result:
                        return result
  
                    half_counts[i] += 1
                    current_prefix.pop()
                    
            memo[state] = ""
            return ""

        current_prefix = []
        return backtrack(0, False)
