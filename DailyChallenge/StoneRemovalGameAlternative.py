class Solution:
    def canAliceWin(self, n: int) -> bool:
        alice = True
        s = 10
        while n >= s:
            n -= s
            s -= 1
            alice = not alice
        return not alice
