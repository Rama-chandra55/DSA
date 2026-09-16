import math
class Solution:
    def numberOfSets(self, n: int, k: int) -> int:
        MOD = 10**9 + 7

        total_slots = n + k - 1

        required_endpoints = 2 * k

        return math.comb(total_slots, required_endpoints) % MOD
