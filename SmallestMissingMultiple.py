class Solution(object):
    def missingMultiple(self, nums, k):
        i=k
        st=[]
        num_set = set(nums)
        while i >= 0 and i <= 200:
            if i % k == 0:
                st.append(i)
                i+=1
            else:
                i+=1
        res=0
        for j in st:
            if j not in num_set:
                res = j
                break
        return res

