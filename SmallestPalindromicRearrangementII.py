import collections

class Solution(object):
    def smallestPalindrome(self, s, k):
        counts = collections.Counter(s)
        # Validate structural validity for a palindrome
        mid = [c for c, v in counts.iteritems() if v % 2]
        if len(mid) > 1: return ""
        
        # Build the exact counts needed for the left half
        left_counts = {c: v // 2 for c, v in counts.iteritems() if v // 2}
        total_len = sum(left_counts.values())
        
        LIMIT = 10**6 + 2
        
        # Fast multinomial counting with early exit to avoid heavy factorials
        def get_perms():
            rem = sum(left_counts.itervalues())
            ans = 1
            for c in left_counts.itervalues():
                if c <= 0: continue
                # Compute comb(rem, c) incrementally with early exit
                k_val = min(c, rem - c)
                comb = 1
                for i in xrange(1, k_val + 1):
                    comb = comb * (rem - i + 1) / i
                    if ans * comb > LIMIT:
                        return LIMIT
                ans *= comb
                rem -= c
            return ans

        # Build left half character by character (sorted alphabetically)
        left_half = []
        for _ in xrange(total_len):
            for c in sorted(left_counts.iterkeys()):
                if left_counts[c] <= 0: continue
                left_counts[c] -= 1
                perms = get_perms()
                if k <= perms:
                    left_half.append(c)
                    break
                k -= perms
                left_counts[c] += 1
            else: return "" # Safeguard if k is completely out of bounds
            
        res = "".join(left_half)
        return res + ("".join(mid) if mid else "") + res[::-1]
