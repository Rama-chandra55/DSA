class Solution:
    def distinctSubseqII(self, s: str) -> int:
        MOD = 10**9 + 7

        ends_in = [0] * 26
        
        for char in s:
            char_idx = ord(char) - ord('a')
   
            ends_in[char_idx] = (sum(ends_in) + 1) % MOD
      
        return sum(ends_in) % MOD
