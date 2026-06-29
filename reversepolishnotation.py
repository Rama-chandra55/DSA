class Solution(object):
    def evalRPN(self, tokens):
        st = []
        l = ['+', '-', '*', '/']
        for i in tokens:
            if i not in l:
                st.append(int(i))
            else:
                a=st.pop()
                b=st.pop()
                if i == '+':
                    st.append(a+b)
                elif i == '-':
                    st.append(b-a)
                elif i == '*':
                    st.append(a*b)
                elif i == '/':
                    st.append(int(float(b)/a))
        return st[-1]
        
