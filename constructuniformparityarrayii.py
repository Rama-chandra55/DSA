class Solution:
    def uniformArray(self, nums1: list[int]) -> bool:
        min_odd = min((x for x in nums1 if x % 2 != 0), default=None)

        if min_odd is None:
            return True

        for x in nums1:
            if x % 2 == 0 and x < min_odd:
                return False
                
        return True
