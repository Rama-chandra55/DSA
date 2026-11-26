class Solution:
    def canAliceWin(self, n: int) -> bool:
        req = 10
        turn = 0
        while n >= req:
            n -= req
            req -= 1
            turn += 1
        return turn % 2 == 1
