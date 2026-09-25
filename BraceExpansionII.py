class Solution:
    def braceExpansionII(self, expression: str) -> list[str]:
        stack, small = [], [set(), {""}]
        
        for char in expression:
            if char.isalpha():
                small[1] = {p + char for p in small[1]}
            elif char == '{':
                stack.append(small)
                small = [set(), {""}]
            elif char == '}':
                prev_union, prev_prod = stack.pop()
                inner_set = small[0] | small[1]
                small = [prev_union, {p + s for p in prev_prod for s in inner_set}]
            elif char == ',':
                small = [small[0] | small[1], {""}]
                
        return sorted(small[0] | small[1])
