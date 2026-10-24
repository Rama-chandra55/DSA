class Solution:
    def countDaysTogether(self, arrA: str, lvA: str, arrB: str, lvB: str) -> int:
        days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        def to_day(d_str: str) -> int:
            m, d = map(int, d_str.split("-"))
            return sum(days[: m - 1]) + d

        stA, edA = to_day(arrA), to_day(lvA)
        stB, edB = to_day(arrB), to_day(lvB)

        st, ed = max(stA, stB), min(edA, edB)
        return max(0, ed - st + 1)
