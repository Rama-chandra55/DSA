# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def nodesBetweenCriticalPoints(self, head: Optional[ListNode]) -> List[int]:
        if not head or not head.next or not head.next.next:
            return [-1, -1]
        
        # Track crucial positional metrics
        first_cp = -1
        prev_cp = -1
        min_dist = float('inf')
        
        # Iteration pointers
        prev = head
        curr = head.next
        idx = 1
        
        while curr.next:
            nxt = curr.next
            
            # Identify local maxima or local minima
            is_max = curr.val > prev.val and curr.val > nxt.val
            is_min = curr.val < prev.val and curr.val < nxt.val
            
            if is_max or is_min:
                if first_cp == -1:
                    # Establish the baseline for maximum distance calculations
                    first_cp = idx
                else:
                    # Update local minimum interval with adjacent critical point
                    min_dist = min(min_dist, idx - prev_cp)
                
                # Cache the current index as the latest critical anchor point
                prev_cp = idx
                
            prev = curr
            curr = nxt
            idx += 1
            
        # Return default state if we failed to locate at least two critical points
        if min_dist == float('inf'):
            return [-1, -1]
            
        return [min_dist, prev_cp - first_cp]
