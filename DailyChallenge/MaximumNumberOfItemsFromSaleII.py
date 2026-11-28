class Solution:
    def maximumSaleItems(self, items: list[list[int]], budget: int) -> int:
        max_factor = max(factor for factor, _ in items)
        min_price = min(price for _, price in items)

        freq = [0] * (max_factor + 1)
        for factor, _ in items:
            freq[factor] += 1

        gains = [0] * (max_factor + 1)
        for factor in range(1, max_factor + 1):
            total = 0
            for multiple in range(factor, max_factor + 1, factor):
                total += freq[multiple]
            gains[factor] = total - 1

        boosted = sorted(
            (price, gains[factor])
            for factor, price in items
            if gains[factor] > 0 and price < 2 * min_price
        )

        remaining = budget
        answer = 0

        for price, count in boosted:
            if remaining < price:
                break
            take = min(count, remaining // price)
            answer += 2 * take
            remaining -= take * price

        answer += remaining // min_price
        return answer
