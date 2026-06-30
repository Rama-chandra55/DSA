class Solution(object):
    def numberOfSubstrings(self, s):
        last_seen = {'a': -1, 'b': -1, 'c': -1}
        count = 0
        for i, char in enumerate(s):
            last_seen[char] = i
            
            if last_seen['a'] != -1 and last_seen['b'] != -1 and last_seen['c'] != -1:
                count += min(last_seen.values()) + 1
                
        return count
