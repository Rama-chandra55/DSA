class Solution:
    def maxPalindromes(self, s: str, k: int) -> int:
        n = len(s)
        ans = 0
        i = 0
        
        while i < n:

            if i + k <= n:
                sub1 = s[i : i + k]
                if sub1 == sub1[::-1]:
                    ans += 1
                    i += k  
                    continue

            if i + k + 1 <= n:
                sub2 = s[i : i + k + 1]
                if sub2 == sub2[::-1]:
                    ans += 1
                    i += k + 1  
                    continue
            i += 1
            
        return ans
