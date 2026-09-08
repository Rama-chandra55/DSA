class Solution:
    def countCommas(self, n: int) -> int:
        if len(str(n)) < 4:
            return 0
        else:
            cnt = 0
            while n > 0:
                a = len(str(n))
                if a > 3:
                    cnt += (a - 1) // 3
                n -= 1
            return cnt
        

