class Solution:
    def evaluate(self, s: str, knowledge: list[list[str]]) -> str:
        d = {k: v for k, v in knowledge}
        res, key, cur = [], [], False
        
        for c in s:
            if c == '(':
                cur = True
            elif c == ')':
                cur = False
                res.append(d.get("".join(key), "?"))
                key = []
            elif cur:
                key.append(c)
            else:
                res.append(c)
                
        return "".join(res)
