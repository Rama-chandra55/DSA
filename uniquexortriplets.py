class Solution:
    def uniqueXorTriplets(self, nums: List[int]) -> int:
        return  1 if  len(sn:= set(nums))<2  else len({
            x^y for x in {a^b for a,b in combinations(sn,2)} for y in sn
        })
