class Solution:
    def countCommas(self, n: int) -> int:
        threshold = 1000
        cnt = 0
        while n >= threshold:
            cnt += (n - threshold + 1)
            threshold *= 1000
        return cnt
