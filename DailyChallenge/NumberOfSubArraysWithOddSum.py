class Solution:
    def numOfSubarrays(self, arr: list[int]) -> int:
        ans = cur = 0
        count = [1, 0]
        for x in arr:
            cur ^= x & 1
            ans += count[1 - cur]
            count[cur] += 1
        return ans % (10**9 + 7)
