nums = [2,7,11,15]
target = 9
num_map = {}
for i, num in enumerate(nums):
    compl = target - num
    if compl in num_map:
        print([num_map[compl], i])
    num_map[num] = i
