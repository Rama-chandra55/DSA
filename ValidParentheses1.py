class Solution(object):
    def isValid(self, s):
        d = {'(':')', '{':'}', '[':']'}
        st=[]
        for i in s:
            if i in d:
                st.append(i)
            else:
                if not st or d[st.pop()] != i:
                    return False
        return len(st) == 0
        
