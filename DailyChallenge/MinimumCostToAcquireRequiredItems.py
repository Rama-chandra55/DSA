# LeetCode: https://leetcode.com/problems/minimum-cost-to-acquire-required-items/
# Problem ID: 3789

class Solution:
    def minimumCost(
        self, cost1: int, cost2: int, costBoth: int, need1: int, need2: int
    ) -> int:
        cost1 = min(cost1, costBoth)
        cost2 = min(cost2, costBoth)
        costBoth = min(costBoth, cost1 + cost2)
        common = min(need1, need2)
        return (
            common * costBoth
            + (need1 - common) * cost1
            + (need2 - common) * cost2
        )
