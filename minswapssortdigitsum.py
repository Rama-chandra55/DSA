class Solution:
    def minSwaps(self, nums: list[int]) -> int:
        def get_dsum(x):
            s = 0
            while x > 0:
                s += x % 10
                x //= 10
            return s
            
        # Target sorted order based on digit sum, breaking ties with the value itself
        tgt = sorted(nums, key=lambda x: (get_dsum(x), x))
        
        # Map each value to its final target position index
        pos = {v: i for i, v in enumerate(tgt)}
        
        ans = 0
        vis = [False] * len(nums)
        
        for i in range(len(nums)):
            if vis[i] or pos[nums[i]] == i:
                continue
                
            # Track the size of the current permutation cycle
            c_sz = 0
            j = i
            while not vis[j]:
                vis[j] = True
                j = pos[nums[j]]
                c_sz += 1
                
            if c_sz > 1:
                ans += c_sz - 1
                
        return ans
