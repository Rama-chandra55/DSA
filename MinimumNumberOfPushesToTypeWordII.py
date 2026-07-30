import collections
class Solution(object):
    def minimumPushes(self, word):
        counts = collections.Counter(word)
        freq = sorted(counts.values(), reverse=True)
        tot = 0
        for i, freq in enumerate(freq):
            press = (i//8) + 1
            tot += freq * press
        return tot

        
