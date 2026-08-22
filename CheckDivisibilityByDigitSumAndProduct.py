class Solution(object):
    def checkDivisibility(self, n):
        res1=0
        res2=1
        for i in str(n):
            a = int(i)
            res1 += a  # 1
            res2 *= a  # 0
        if n % (res1+res2) == 0:
            return True
        else:
            return False
