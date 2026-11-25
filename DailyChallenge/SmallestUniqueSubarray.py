class Solution:
    def smallestUniqueSubarray(self, nums):
        n = len(nums)
        if n == 1:
            return 1

        values = sorted(set(nums))
        value_rank = {value: index + 1 for index, value in enumerate(values)}
        rank = [value_rank[value] for value in nums]
        classes = len(values)
        suffixes = sorted(range(n), key=lambda i: rank[i])

        def counting_sort(indices, key_func, class_count):
            count = [0] * (class_count + 1)
            for index in indices:
                count[key_func(index)] += 1

            total = 0
            for i, frequency in enumerate(count):
                count[i] = total
                total += frequency

            result = [0] * len(indices)
            for index in indices:
                key = key_func(index)
                result[count[key]] = index
                count[key] += 1
            return result

        length = 1
        while length < n and classes < n:
            suffixes = counting_sort(
                suffixes,
                lambda i: rank[i + length] if i + length < n else 0,
                classes,
            )
            suffixes = counting_sort(suffixes, lambda i: rank[i], classes)

            new_rank = [0] * n
            new_classes = 1
            new_rank[suffixes[0]] = new_classes

            for i in range(1, n):
                previous = suffixes[i - 1]
                current = suffixes[i]
                previous_pair = (
                    rank[previous],
                    rank[previous + length]
                    if previous + length < n else 0,
                )
                current_pair = (
                    rank[current],
                    rank[current + length]
                    if current + length < n else 0,
                )
                if current_pair != previous_pair:
                    new_classes += 1
                new_rank[current] = new_classes

            rank = new_rank
            classes = new_classes
            length <<= 1

        position = [0] * n
        for i, start in enumerate(suffixes):
            position[start] = i

        lcp = [0] * n
        common = 0
        for start in range(n):
            order = position[start]
            if order == 0:
                common = 0
                continue

            previous = suffixes[order - 1]
            while (
                start + common < n
                and previous + common < n
                and nums[start + common] == nums[previous + common]
            ):
                common += 1

            lcp[order] = common
            if common:
                common -= 1

        answer = n
        for order, start in enumerate(suffixes):
            longest = lcp[order]
            if order + 1 < n:
                longest = max(longest, lcp[order + 1])

            candidate = longest + 1
            if candidate <= n - start:
                answer = min(answer, candidate)

        return answer
