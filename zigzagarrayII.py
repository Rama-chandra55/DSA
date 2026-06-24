class Solution(object):
    def zigZagArrays(self, n, l, r):
        MOD = 10**9 + 7
        M = r - l + 1
        
        if n == 1:
            return M
            
        dim = 2 * M
    
        T = [[0] * dim for _ in range(dim)]
        
        for curr_val in range(M):
    
            for next_val in range(curr_val + 1, M):
                next_state = next_val
                prior_state = M + curr_val
                T[next_state][prior_state] = 1
         
            for next_val in range(curr_val):
                next_state = M + next_val
                prior_state = curr_val
                T[next_state][prior_state] = 1

        def multiply(A, B):
            C = [[0] * dim for _ in range(dim)]
            for i in range(dim):
                for k in range(dim):
                    if A[i][k] == 0:
                        continue
                    for j in range(dim):
                        if B[k][j] == 0:
                            continue
                        C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % MOD
            return C

        def power(matrix, p):
            result = [[0] * dim for _ in range(dim)]
            for i in range(dim):
                result[i][i] = 1  
                
            base = matrix
            while p > 0:
                if p % 2 == 1:
                    result = multiply(result, base)
                base = multiply(base, base)
                p //= 2
            return result

        T_pow = power(T, n - 2)
      
        initial_dp = [0] * dim
        for v1 in range(M):
            for v2 in range(M):
                if v1 < v2:
                    initial_dp[v2] += 1   
                elif v1 > v2:
                    initial_dp[M + v2] += 1  

        final_dp = [0] * dim
        for i in range(dim):
            total = 0
            for j in range(dim):
                if T_pow[i][j] != 0 and initial_dp[j] != 0:
                    total = (total + T_pow[i][j] * initial_dp[j]) % MOD
            final_dp[i] = total
            
        return sum(final_dp) % MOD
        
