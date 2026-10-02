class Solution:
    def generateParenthesis(self, n):
        ans = []
        def dfs(s, o, c):
            if len(s) == 2 * n:
                ans.append(s)
                return
            
            if o < n:
                dfs(s + "(", o + 1, c)
                
            if c < o:
                dfs(s + ")", o, c + 1)
                
        dfs("", 0, 0)
        return ans
