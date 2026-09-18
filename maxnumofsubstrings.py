class Solution:
    def maxNumOfSubstrings(self, s: str) -> list[str]:
        first = {c: i for i, c in enumerate(s) if c not in s[:i]}
        last = {c: i for i, c in enumerate(s)}

        def get_valid_end(i: int) -> int:
            end = last[s[i]]
            j = i
            while j <= end:

                if first[s[j]] < i:
                    return -1

                end = max(end, last[s[j]])
                j += 1
            return end

        intervals = []
        for c in set(s):
            i = first[c]
            end = get_valid_end(i)
            if end != -1:
                intervals.append((i, end))

        intervals.sort(key=lambda x: x[1])
        
        res = []
        prev_end = -1
        
        for start, end in intervals:

            if start > prev_end:
                res.append(s[start : end + 1])
                prev_end = end
                
        return res
