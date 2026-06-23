class Solution(object):
    def zigZagArrays(self, n, l, r):
        MOD = 10**9 + 7
        m = r - l + 1
        if m == 1:
            return 1 if n == 1 else 0

        dp_up = [0] * m
        dp_down = [0] * m
        
        for v in range(m):
            dp_up[v] = v 
            dp_down[v] = m - 1 - v 
            
        for _ in range(3, n + 1):
            next_up = [0] * m
            next_down = [0] * m
            curr_sum_down = 0
            for v in range(m):
                next_up[v] = curr_sum_down % MOD
                curr_sum_down += dp_down[v]

            curr_sum_up = 0
            for v in range(m - 1, -1, -1):
                next_down[v] = curr_sum_up % MOD
                curr_sum_up += dp_up[v]
                
            dp_up = next_up
            dp_down = next_down
            
        return (sum(dp_up) + sum(dp_down)) % MOD
        
