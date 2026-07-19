class Solution(object):
    def smallestSubsequence(self, s):
        last_occurrence = {}
        for i, char in enumerate(s):
            last_occurrence[char] = i
   
        stack = []
        seen = set()

        for i, char in enumerate(s):
  
            if char in seen:
                continue
     
            while stack and stack[-1] > char and last_occurrence[stack[-1]] > i:
                removed_char = stack.pop()
                seen.remove(removed_char)
           
            stack.append(char)
            seen.add(char)
    
        return "".join(stack)
