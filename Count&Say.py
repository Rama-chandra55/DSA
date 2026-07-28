from itertools import groupby
class Solution(object):
    def countAndSay(self, n):
        if n == 1:
            return "1"
        else:
            curr = "1"
            for _ in range(n-1):
                curr = "".join(str(len(list(group))) + key for key, group in groupby(curr))
            return curr
                 
        
