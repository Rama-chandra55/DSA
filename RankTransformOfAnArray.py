class Solution(object):
    def arrayRankTransform(self, arr):
        freq={}
        rank=1
        arr2=sorted(arr)
        for i in range(len(arr2)):
            if arr2[i] not in freq:
                freq[arr2[i]]=rank
                rank+=1 
        res=[]
        for i in range(len(arr)):
            res.append(freq[arr[i]])
        return res
        
