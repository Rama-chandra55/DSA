class Solution(object):
    def lengthOfLastWord(self, s):
        words = s.split()
        cnt=0
        for i in words[-1]:
            cnt+=1
        return cnt

        
