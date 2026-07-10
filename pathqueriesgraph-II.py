class Solution(object):
    def pathExistenceQueries(self, n, nums, maxDiff, queries):
        arr = sorted((nums[i], i) for i in range(n))

        pos = [0] * n
        comp = [0] * n

        cid = 0
        for i in range(n):
            if i > 0 and arr[i][0] - arr[i - 1][0] > maxDiff:
                cid += 1
            pos[arr[i][1]] = i
            comp[arr[i][1]] = cid

        nxt = [0] * n
        r = 0
        for l in range(n):
            while r + 1 < n and arr[r + 1][0] - arr[l][0] <= maxDiff:
                r += 1
            nxt[l] = r

        LOG = 17
        up = [nxt]
        for _ in range(1, LOG):
            prev = up[-1]
            cur = [0] * n
            for i in range(n):
                cur[i] = prev[prev[i]]
            up.append(cur)

        ans = []

        for u, v in queries:
            if u == v:
                ans.append(0)
                continue

            if comp[u] != comp[v]:
                ans.append(-1)
                continue

            a = pos[u]
            b = pos[v]

            if a > b:
                a, b = b, a

            if a == b:
                ans.append(0)
                continue

            cur = a
            steps = 0

            for k in range(LOG - 1, -1, -1):
                if up[k][cur] < b:
                    cur = up[k][cur]
                    steps += 1 << k

            ans.append(steps + 1)

        return ans
        
