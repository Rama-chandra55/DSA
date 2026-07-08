class Solution(object):
    def sumAndMultiply(self, s, queries):
        MOD = 10 ** 9 + 7
        n = len(s)

        pref_sum = [0] * (n + 1)

        prev_nonzero = [-1] * n
        last = -1
        for i in range(n):
            d = ord(s[i]) - ord('0')
            pref_sum[i + 1] = pref_sum[i] + (d if d != 0 else 0)
            if d != 0:
                last = i
            prev_nonzero[i] = last

        next_nonzero = [n] * n
        nxt = n
        for i in range(n - 1, -1, -1):
            if s[i] != '0':
                nxt = i
            next_nonzero[i] = nxt

        pow10 = [1] * (n + 1)
        for i in range(1, n + 1):
            pow10[i] = (pow10[i - 1] * 10) % MOD

        pref_hash = [0]
        nonzero_rank = [-1] * n
        cnt = 0
        for i in range(n):
            if s[i] != '0':
                pref_hash.append((pref_hash[-1] * 10 + int(s[i])) % MOD)
                nonzero_rank[i] = cnt
                cnt += 1

        ans = []

        for l, r in queries:
            first = next_nonzero[l]
            if first > r:
                ans.append(0)
                continue

            last = prev_nonzero[r]

            left_rank = nonzero_rank[first]
            right_rank = nonzero_rank[last]

            length = right_rank - left_rank + 1

            x = (
                pref_hash[right_rank + 1]
                - pref_hash[left_rank] * pow10[length]
            ) % MOD

            digit_sum = pref_sum[r + 1] - pref_sum[l]

            ans.append((x * digit_sum) % MOD)

        return ans
