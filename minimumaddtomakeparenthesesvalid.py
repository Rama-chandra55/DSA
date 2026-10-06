class Solution:
    def minAddToMakeValid(self, s: str) -> int:
        ans = bal = 0
        for c in s:
            bal += 1 if c == '(' else -1
            if bal == -1:
                ans += 1
                bal = 0
        return ans + bal
