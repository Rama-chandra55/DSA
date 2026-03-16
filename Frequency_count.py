arr = [1,2,2,3,3,3,4]
freq = {}
for num in arr:
    if num in freq:
        freq[num] += 1
    else:
        freq[num] = 1
for key, value in freq.items():
    print(key, "->", value)
