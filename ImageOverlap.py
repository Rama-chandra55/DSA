class Solution:
    def largestOverlap(self, img1: List[List[int]], img2: List[List[int]]) -> int:
        list1 = [(r, c) for r, row in enumerate(img1) for c, val in enumerate(row) if val == 1]
        list2 = [(r, c) for r, row in enumerate(img2) for c, val in enumerate(row) if val == 1]

        if not list1 or not list2:
            return 0

        transformation_counts = Counter()
        for r1, c1 in list1:
            for r2, c2 in list2:
                shift_vector = (r2 - r1, c2 - c1)
                transformation_counts[shift_vector] += 1

        return max(transformation_counts.values())
