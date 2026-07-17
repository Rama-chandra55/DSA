from collections import Counter
from math import comb
from bisect import bisect_right
class Solution:
    def gcdValues(self, nums: List[int], queries: List[int]) -> List[int]:
        cnt = Counter(nums)
        M = max(cnt)
        
        # Count pairs with actual GCD equal to d
        gcd_cnt = [0] * (M + 1)
        for d in range(M, 0, -1):
            mults = sum(cnt[m] for m in range(d, M + 1, d))
            gcd_cnt[d] = comb(mults, 2) - sum(gcd_cnt[2*d::d])
            
        # Accumulate prefix sums of pair counts
        pref = [0] * (M + 2)
        for i in range(1, M + 1):
            pref[i] = pref[i-1] + gcd_cnt[i]
            
        return [bisect_right(pref, q, 0, M + 1) for q in queries]
