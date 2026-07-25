class Solution(object):
    def maxProduct(self, n):
        lr=sr=float('-inf')
        for i in str(n):
            a=int(i)
            if a > lr:  
                sr = lr  
                lr = a  
            elif a > sr:
                sr = a
        res = lr*sr
        return res
        
