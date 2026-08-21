import math
from itertools import combinations
from typing import List
class Solution:
    def findKthSmallest(self, coins: List[int], k: int) -> int:
        subsets_lcm = []
        n = len(coins)
        
        for r in range(1, n + 1):
            for combo in combinations(coins, r):
                # Calculate LCM for the current combination of coins
                current_lcm = combo[0]
                for coin in combo[1:]:
                    current_lcm = (current_lcm * coin) // math.gcd(current_lcm, coin)
                
                # Store the LCM along with the subset size (to check odd/even)
                subsets_lcm.append((current_lcm, r))
                
        def count_multiples(target: int) -> int:
            """Counts how many unique multiples of coins are <= target."""
            count = 0
            for lcm, size in subsets_lcm:
                # Principle of Inclusion-Exclusion
                if size % 2 == 1:
                    count += target // lcm
                else:
                    count -= target // lcm
            return count

        # Binary search range for the kth smallest amount
        low = 1
        high = min(coins) * k
        ans = high
        
        while low <= high:
            mid = (low + high) // 2
            if count_multiples(mid) >= k:
                ans = mid
                high = mid - 1
            else:
                low = mid + 1
                
        return ans
