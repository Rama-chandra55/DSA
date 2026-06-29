class Solution(object):
    def numOfStrings(self, patterns, word):
        return sum(1 for p in patterns if p in word)
        
