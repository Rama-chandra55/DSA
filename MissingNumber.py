def missing_number(nums: list[int]) -> int:
    n = len(nums)
    expected_sum = n * (n + 1) // 2
    actual_sum = sum(nums)
    return expected_sum - actual_sum
def missing_number_xor(nums: list[int]) -> int:
    res = len(nums)
    for i, num in enumerate(nums):
        res ^= i ^ num
    return res
print(missing_number([3,0,1]))         # 2
print(missing_number_xor([9,6,4,2,3,5,7,0,1]))  # 8
