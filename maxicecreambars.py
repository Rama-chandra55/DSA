class Solution(object):
    def maxIceCream(self, costs, coins):
        sum=0
        count=0
        costs.sort()
        for i in costs:
            if i <= coins:
                count +=1
                sum += i
                coins -= i
        return count

        
