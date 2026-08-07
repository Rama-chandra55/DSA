Fix smallest divisible digit product solution

class Solution:
    def smallestNumber(self, num: str, t: int) -> str:
        p = [2, 3, 5, 7]
        need = [0] * 4

        for i, x in enumerate(p):
            while t % x == 0:
                need[i] += 1
                t //= x

        if t > 1:
            return "-1"

        f = [
            (0,0,0,0), (0,0,0,0), (1,0,0,0), (0,1,0,0),
            (2,0,0,0), (0,0,1,0), (1,1,0,0), (0,0,0,1),
            (3,0,0,0), (0,2,0,0)
        ]

        A, B = need[0], need[1]

        dp = [[99] * (B + 1) for _ in range(A + 1)]
        dp[0][0] = 0

        for a in range(A + 1):
            for b in range(B + 1):
                for d in range(2, 10):
                    x = max(0, a - f[d][0])
                    y = max(0, b - f[d][1])
                    dp[a][b] = min(dp[a][b], 1 + dp[x][y])

        def mn(r):
            return dp[r[0]][r[1]] + r[2] + r[3]

        def build(r, n):
            ans = ""
            for i in range(n):
                for d in range(1, 10):
                    nr = [max(0, r[j] - f[d][j]) for j in range(4)]
                    if mn(nr) <= n - i - 1:
                        ans += str(d)
                        r = nr
                        break
            return ans

        # Already valid
        cur = [0] * 4
        zero = False

        for c in num:
            d = int(c)
            if d == 0:
                zero = True
            for j in range(4):
                cur[j] += f[d][j]

        if not zero and all(cur[j] >= need[j] for j in range(4)):
            return num

        # Try same length
        pref = [[0] * 4]
        zeros = [0]

        for c in num:
            d = int(c)
            pref.append([pref[-1][j] + f[d][j] for j in range(4)])
            zeros.append(zeros[-1] + (d == 0))

        for i in range(len(num) - 1, -1, -1):
            if zeros[i]:
                continue

            for d in range(int(num[i]) + 1, 10):
                r = [
                    max(0, need[j] - pref[i][j] - f[d][j])
                    for j in range(4)
                ]

                left = len(num) - i - 1

                if mn(r) <= left:
                    return num[:i] + str(d) + build(r, left)

        # Need more digits than num
        length = max(len(num) + 1, mn(need))
        return build(need, length)
