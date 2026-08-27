from collections import Counter

class Solution:
    def lexGreaterPermutation(self, s: str, target: str) -> str:
        n = len(s)
        count = Counter(s)

        matched = 0
        for i in range(n):
            ch = target[i]
            if count[ch] > 0:
                count[ch] -= 1
                matched += 1
            else:
                break

        for pos in range(matched, -1, -1):
   
            if pos < matched:
                count[target[pos]] += 1

            if pos == n:
                continue
                
            target_char_code = ord(target[pos])

            for c_code in range(target_char_code + 1, ord('z') + 1):
                ch_candidate = chr(c_code)
                if count[ch_candidate] > 0:

                    prefix = target[:pos]
   
                    mid = ch_candidate
                    count[ch_candidate] -= 1
            
                    suffix = []
                    for code in range(ord('a'), ord('z') + 1):
                        char = chr(code)
                        if count[char] > 0:
                            suffix.append(char * count[char])
                    
                    return prefix + mid + "".join(suffix)
                    
        return ""
