class Solution(object):
    def pathExistenceQueries(self, n, nums, maxDiff, queries):
        component = [0] * n
        comp = 0

        for i in range(1, n):
            if nums[i] - nums[i - 1] > maxDiff:
                comp += 1
            component[i] = comp

        return [component[u] == component[v] for u, v in queries]
        
