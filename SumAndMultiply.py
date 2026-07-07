class Solution(object):
    def sumAndMultiply(self, n):
        st=[]
        for i in str(n):
            if i != '0':
                st.append(int(i))
        cnt=0
        for a in st:
            cnt+=a
        val = "".join(str(x) for x in st)
        if not val:
            return 0
        res = int(val) * cnt
        return res


        
