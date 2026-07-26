class Solution(object):
    def maximumProduct(self, nums):
        lr=scr=thr=float('-inf')
        sm1=sm2=float('inf')
        for i in nums:
            if i > lr:
                thr = scr
                scr = lr
                lr = i
            elif i > scr:
                thr = scr
                scr = i
            elif i > thr:
                thr = i
            if i < sm1:
                sm2 = sm1
                sm1 = i
            elif i < sm2:
                sm2 = i
        res = max(thr*scr*lr, sm2*sm1*lr)
        return res
        
