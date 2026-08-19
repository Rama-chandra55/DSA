from collections import defaultdict
class Solution:
    def maxNumberOfFamilies(self, n: int, reservedSeats: list[list[int]]) -> int:

        reserved = defaultdict(int)
        for row, col in reservedSeats:
            if 2 <= col <= 9:

                reserved[row] |= (1 << (col - 2))

        ans = n * 2 

        LEFT_MASK = 15
        RIGHT_MASK = 240
        MIDDLE_MASK = 60
        
        for mask in reserved.values():
            left_free = (mask & LEFT_MASK) == 0
            right_free = (mask & RIGHT_MASK) == 0
            middle_free = (mask & MIDDLE_MASK) == 0
 
            if left_free and right_free:
                continue
            elif left_free or right_free or middle_free:
                ans -= 1 
            else:
                ans -= 2 
                
        return ans
