class Solution(object):
    def smallestNumber(self, n, t):
        i=n
        while i>=n:
            s = str(i)
            pt=1
            for j in s:
                pt *= int(j)
            if pt%t == 0:
                return i
            i+=1
        
