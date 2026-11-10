class FenwickTree:
    def __init__(self, size):
        self.size = size
        self.tree = [0] * (size + 1)

    def update(self, index, delta):
        # Add delta to element at 1-based index
        while index <= self.size:
            self.tree[index] += delta
            index += index & (-index)

    def query(self, index):
        # Return prefix sum from index 1 to index
        total = 0
        while index > 0:
            total += self.tree[index]
            index -= index & (-index)
        return total

    def range_query(self, left, right):
        # Return sum of elements between left and right (inclusive)
        return self.query(right) - self.query(left - 1)


if __name__ == "__main__":
    data = [3, 2, -1, 6, 5, 4, -3, 3, 7, 2]
    bit = FenwickTree(len(data))

    for i, val in enumerate(data, start=1):
        bit.update(i, val)

    print("Sum of first 5 elements:", bit.query(5))
    print("Sum from index 3 to 7:", bit.range_query(3, 7))

    # Update index 4 by adding +3
    bit.update(4, 3)
    print("Updated sum of first 5 elements:", bit.query(5))
