class Solution(object):
    def minimumPushes(self, word):
        n = len(word)
        
        if n <= 8:
            return n
        if n <= 16:
            return 8 + (n - 8) * 2
        if n <= 24:
            return 8 + 16 + (n - 16) * 3
            
        return 8 + 16 + 24 + (n - 24) * 4
        
