class Solution:
    def reverseParentheses(self, s: str) -> str:
        stack = []
        for c in s:
            if c == ")":
                parenthesis = ""
                while stack[-1] != "(":
                    parenthesis += stack.pop()[::-1]
                stack.pop() 
                stack.append(parenthesis)
            else:
                stack.append(c)
        return "".join(stack)
