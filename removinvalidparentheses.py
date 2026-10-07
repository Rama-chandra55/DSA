class Solution:
    def removeInvalidParentheses(self, s: str) -> list[str]:
        l = r = 0
        for c in s:
            if c == '(': l += 1
            elif c == ')':
                if l > 0: l -= 1
                else: r += 1
        res = set()
        def dfs(i, nl, nr, o, p):
            if i == len(s):
                if not nl and not nr and not o: res.add("".join(p))
                return
            if o < 0: return
            c = s[i]
            if c == '(' and nl > 0: dfs(i + 1, nl - 1, nr, o, p)
            elif c == ')' and nr > 0: dfs(i + 1, nl, nr - 1, o, p)
            p.append(c)
            if c == '(': dfs(i + 1, nl, nr, o + 1, p)
            elif c == ')': dfs(i + 1, nl, nr, o - 1, p)
            else: dfs(i + 1, nl, nr, o, p)
            p.pop()
        dfs(0, l, r, 0, [])
        return list(res)
