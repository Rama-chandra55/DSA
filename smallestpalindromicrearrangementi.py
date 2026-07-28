class Solution(object):
    def smallestPalindrome(self, s):
        if len(s) == 1:
            return s
        else:
            n=len(s)
            first_half = "".join(sorted(s[:n//2]))
            middle = s[n//2] if n%2 != 0 else ""
            last = first_half[::-1]
            return first_half + middle + last
        
