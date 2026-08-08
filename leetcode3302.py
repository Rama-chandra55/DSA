n, m = len(word1), len(word2)
        
        # last[j] stores the maximum index i in word1 that matches word2[j]
        # such that the remaining suffix of word2 can be successfully matched.
        last = [-1] * m
        i, j = n - 1, m - 1
        while i >= 0 and j >= 0:
            if word1[i] == word2[j]:
                last[j] = i
                j -= 1
            i -= 1
            
        ans = []
        can_skip = True
        j = 0
        
        for i in range(n):
            if j == m:
                break
                
            if word1[i] == word2[j]:
                ans.append(i)
                j += 1
            elif can_skip:
                # Check if suffix can match after using our one allowed substitution
                if j + 1 == m or last[j + 1] > i:
                    ans.append(i)
                    can_skip = False
                    j += 1
                    
        return ans if j == m else []
