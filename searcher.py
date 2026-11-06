def binary_search(arr, target):
    """Finds the index of a target in a sorted array, or returns -1."""
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


if __name__ == "__main__":
    nums = [1, 3, 5, 7, 9, 11]
    print(f"Index of 7: {binary_search(nums, 7)}")
