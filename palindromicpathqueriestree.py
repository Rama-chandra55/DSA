class SegTree:

    def __init__(self, n):
        self.n = n
        self.t = [0] * (2 * n)

    def up(self, p, v):
        p += self.n
        self.t[p] = v
        while p > 1:
            p >>= 1
            self.t[p] = self.t[2 * p] ^ self.t[2 * p + 1]

    def qry(self, l, r):
        res = 0
        l += self.n
        r += self.n + 1
        while l < r:
            if l & 1:
                res ^= self.t[l]
                l += 1
            if r & 1:
                r -= 1
                res ^= self.t[r]
            l >>= 1
            r >>= 1
        return res


class Solution:

    def palindromicPathQueries(
        self, n: int, edges: list[list[int]], s: str, queries: list[str]
    ) -> list[bool]:
        g = [[] for _ in range(n)]
        for u, v in edges:
            g[u].append(v)
            g[v].append(u)

        par, dep, hvy, hd, pos, sz = (
            [-1] * n,
            [0] * n,
            [-1] * n,
            [0] * n,
            [0] * n,
            [1] * n,
        )
        ord_nodes, st = [], [0]

        while st:
            u = st.pop()
            ord_nodes.append(u)
            for v in g[u]:
                if v != par[u]:
                    par[v], dep[v] = u, dep[u] + 1
                    st.append(v)

        for u in reversed(ord_nodes):
            for v in g[u]:
                if v != par[u]:
                    sz[u] += sz[v]
                    if hvy[u] == -1 or sz[v] > sz[hvy[u]]:
                        hvy[u] = v

        c_pos, st = 0, [(0, 0)]
        while st:
            u, h = st.pop()
            hd[u], pos[u] = h, c_pos
            c_pos += 1
            if hvy[u] != -1:
                for v in g[u]:
                    if v != par[u] and v != hvy[u]:
                        st.append((v, v))
                st.append((hvy[u], h))

        tree = SegTree(n)
        for i in range(n):
            tree.up(pos[i], 1 << (ord(s[i]) - 97))

        def path_mask(u, v):
            m = 0
            while hd[u] != hd[v]:
                if dep[hd[u]] > dep[hd[v]]:
                    u, v = v, u
                m ^= tree.qry(pos[hd[v]], pos[v])
                v = par[hd[v]]
            if dep[u] > dep[v]:
                u, v = v, u
            return m ^ tree.qry(pos[u], pos[v])

        ans = []
        for q in queries:
            p = q.split()
            if p[0] == "update":
                tree.up(pos[int(p[1])], 1 << (ord(p[2]) - 97))
            else:
                m = path_mask(int(p[1]), int(p[2]))
                ans.append((m & (m - 1)) == 0)
        return ans
