class Solution:
    def createGrid(self, m: int, n: int) -> list[str]:
        # The first row is completely free (all '.')
        first_row = "." * n
        
        # Remaining m - 1 rows have obstacles everywhere except the last column
        # So we have (n - 1) '#' followed by a single '.'
        other_row = "#" * (n - 1) + "."
        
        # Combine the first row with m - 1 copies of the other rows
        return [first_row] + [other_row] * (m - 1)
