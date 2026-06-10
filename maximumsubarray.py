class Solution(object):
    def maxTotalValue(self, nums, k):
        n = len(nums)
        logs = [0] * (n + 1)
        for i in range(2, n + 1):
            logs[i] = logs[i >> 1] + 1

        K_pow = logs[n]
        st_min = [[0] * n for _ in range(K_pow + 1)]
        st_max = [[0] * n for _ in range(K_pow + 1)]

        for i in range(n):
            st_min[0][i] = nums[i]
            st_max[0][i] = nums[i]

        for j in range(1, K_pow + 1):
            curr_len = 1 << j
            half_len = 1 << (j - 1)
            for i in range(n - curr_len + 1):
                st_min[j][i] = min(st_min[j-1][i], st_min[j-1][i + half_len])
                st_max[j][i] = max(st_max[j-1][i], st_max[j-1][i + half_len])

        def get_value(l, r):
            length = r - l + 1
            j = logs[length]
            mn = min(st_min[j][l], st_min[j][r - (1 << j) + 1])
            mx = max(st_max[j][l], st_max[j][r - (1 << j) + 1])
            return mx - mn

        pq = []
        for i in range(n):
            val = get_value(i, n - 1)
            heapq.heappush(pq, (-val, i, n - 1))
        
        total_value = 0
        for _ in range(k):
            neg_val, l, r = heapq.heappop(pq)
            total_value += -neg_val
            if l < r:
                next_r = r - 1
                new_val = get_value(l, next_r)
                heapq.heappush(pq, (-new_val, l, next_r))

        return total_value
        
