class Solution:
    def sumCounts(self, A: list[int]) -> int:
        n, M = len(A), 10**9 + 7
        t1, t2, z = [0] * (4 * n), [0] * (4 * n), [0] * (4 * n)
        
        def up(o, l, r, ql, qr):
            if ql <= l and r <= qr:
                t2[o] = (t2[o] + 2 * t1[o] + (r - l + 1)) % M
                t1[o] = (t1[o] + r - l + 1) % M
                z[o] += 1
                return
            m = (l + r) // 2
            if z[o]:
                for c, s in ((2 * o, m - l + 1), (2 * o + 1, r - m)):
                    t2[c] = (t2[c] + 2 * z[o] * t1[c] + z[o]**2 * s) % M
                    t1[c] = (t1[c] + z[o] * s) % M
                    z[c] += z[o]
                z[o] = 0
            if ql <= m: up(2 * o, l, m, ql, qr)
            if qr > m:  up(2 * o + 1, m + 1, r, ql, qr)
            t1[o] = (t1[2 * o] + t1[2 * o + 1]) % M
            t2[o] = (t2[2 * o] + t2[2 * o + 1]) % M

        ans, pos = 0, {}
        for r, x in enumerate(A):
            up(1, 0, n - 1, pos.get(x, -1) + 1, r)
            ans, pos[x] = (ans + t2[1]) % M, r
        return ans
