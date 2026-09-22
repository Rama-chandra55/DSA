class Solution:
    def resultArray(self, nums: list[int], k: int, queries: list[list[int]]) -> list[int]:
        n = len(nums)
        
        P = [1] * (4 * n)                
        R = [[0] * k for _ in range(4 * n)] 

        def merge(u, L, R_node):
            P[u] = (P[L] * P[R_node]) % k
           
            for r in range(k): R[u][r] = R[L][r]
          
            for r in range(k):
                R[u][(P[L] * r) % k] += R[R_node][r]

        def build(u, l, r):
            if l == r:
                v = nums[l] % k
                P[u] = v
                R[u][v] = 1
                return
            m = (l + r) // 2
            build(2 * u + 1, l, m)
            build(2 * u + 2, m + 1, r)
            merge(u, 2 * u + 1, 2 * u + 2)

        def update(u, l, r, idx, val):
            if l == r:
                v = val % k
                P[u] = v
                R[u] = [0] * k
                R[u][v] = 1
                return
            m = (l + r) // 2
            if idx <= m:
                update(2 * u + 1, l, m, idx, val)
            else:
                update(2 * u + 2, m + 1, r, idx, val)
            merge(u, 2 * u + 1, 2 * u + 2)

        def query(u, l, r, ql, qr):
            if ql <= l and r <= qr:
                return P[u], R[u]
            m = (l + r) // 2
            if qr <= m:
                return query(2 * u + 1, l, m, ql, qr)
            if ql > m:
                return query(2 * u + 2, m + 1, r, ql, qr)
            
            lp, lr = query(2 * u + 1, l, m, ql, qr)
            rp, rr = query(2 * u + 2, m + 1, r, ql, qr)
            
            # Temporary merge for cross-range queries
            cur_p = (lp * rp) % k
            cur_r = list(lr)
            for r_idx in range(k):
                cur_r[(lp * r_idx) % k] += rr[r_idx]
            return cur_p, cur_r

        build(0, 0, n - 1)
        ans = []
        for idx, val, start, x in queries:
            update(0, 0, n - 1, idx, val)
            _, rem_counts = query(0, 0, n - 1, start, n - 1)
            ans.append(rem_counts[x])
            
        return ans
