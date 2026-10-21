from itertools import pairwise

class Solution:
    def minOperations(self, s: str) -> int:
        if all(a <= b for a, b in pairwise(s)): return 0
        if len(s) == 2: return -1
        
        l, r = min(s), max(s)
        if s[0] == l or s[-1] == r: return 1
        if any(c in (l, r) for c in s[1:-1]): return 2
        return 3
