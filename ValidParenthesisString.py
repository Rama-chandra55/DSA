class Solution(object):
    def checkValidString(self, s):
        if len(s) == 1 and s != '*':
            return False
        else:
            cnt=0
            for i in s:
                if i == '(':
                    cnt+=1
                elif i == '*':
                    cnt+=1
                if i == ')':
                    cnt-=1
                if cnt < 0:
                    return False
            cnt=0
            for i in reversed(s):
                if i == ')':
                    cnt+=1
                elif i == '*':
                    cnt+=1
                elif i == '(':
                    cnt-=1
                if cnt < 0:
                    return False
        return True
                
                
                    


        
