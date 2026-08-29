class Solution(object):
    def lexicographicallySmallestArray(self, nums, limit):
        sorted_pairs = sorted((num, i) for i, num in enumerate(nums))
        
        # Lists to store our grouped structures
        groups = []
        num_to_group_idx = {}
        
        # 2. Divide elements into swappable groups
        for num, orig_idx in sorted_pairs:
            # Start a new group if it's the first element or breaks the limit condition
            if not groups or num - groups[-1][-1] > limit:
                groups.append(deque())
            
            # Add element to the current group
            groups[-1].append(num)
            # Map the original index to its respective group ID
            num_to_group_idx[orig_idx] = len(groups) - 1
            
        # 3. Reconstruct the answer using the smallest available element for each index
        result = []
        for i in range(len(nums)):
            group_idx = num_to_group_idx[i]
            # Pop the smallest remaining element from this group
            result.append(groups[group_idx].popleft())
            
        return result
