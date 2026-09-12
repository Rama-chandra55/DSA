import bisect
from functools import lru_cache
class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        sorted_intervals = []
        for idx, (l, r, w) in enumerate(intervals):
            sorted_intervals.append((l, r, w, idx))

        sorted_intervals.sort(key=lambda x: x[0])
        n = len(intervals)

        starts = [x[0] for x in sorted_intervals]
        
        @lru_cache(None)
        def dp(i, count):

            if count == 4 or i == n:
                return 0, []

            best_score, best_indices = dp(i + 1, count)

            curr_start, curr_end, curr_weight, curr_idx = sorted_intervals[i]

            next_i = bisect.bisect_right(starts, curr_end)
            
            next_score, next_indices = dp(next_i, count + 1)
            take_score = curr_weight + next_score

            take_indices = sorted([curr_idx] + next_indices)

            if take_score > best_score:
                best_score = take_score
                best_indices = take_indices
            elif take_score == best_score:
                if not best_indices or take_indices < best_indices:
                    best_indices = take_indices
                    
            return best_score, best_indices

        return dp(0, 0)[1]
