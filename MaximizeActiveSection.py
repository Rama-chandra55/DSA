class Solution(object):
    def maxActiveSectionsAfterTrade(self, s):
        total_ones = s.count('1')
        
        # Extract the lengths of all consecutive '0' blocks
        zero_blocks = []
        n = len(s)
        i = 0
        while i < n:
            if s[i] == '0':
                start = i
                while i < n and s[i] == '0':
                    i += 1
                zero_blocks.append(i - start)
            else:
                i += 1
                
        # If there are fewer than 2 zero blocks, no valid trade can surround any '1's
        if len(zero_blocks) < 2:
            return total_ones
            
        # Find the maximum sum of two adjacent '0' blocks
        max_trade_gain = 0
        for j in range(len(zero_blocks) - 1):
            max_trade_gain = max(max_trade_gain, zero_blocks[j] + zero_blocks[j+1])
            
        return total_ones + max_trade_gain
        
