class Solution(object):
    def shiftGrid(self, grid, k):
        m, n = len(grid), len(grid[0])
        total_elements = m * n
        
        # Create an empty target grid of the exact same dimensions
        result = [[0] * n for _ in range(m)]
        
        # Reduce k to avoid redundant full-grid rotations
        k %= total_elements
        
        for i in range(m):
            for j in range(n):
                # Convert 2D index (i, j) to its flattened 1D array position
                flat_index = i * n + j
                
                # Apply the shift and handle wrap-around with modulo
                new_flat_index = (flat_index + k) % total_elements
                
                # Convert the new 1D index back into 2D coordinates (row, col)
                new_row, new_col = divmod(new_flat_index, n)
                
                # Place the element into its final location
                result[new_row][new_col] = grid[i][j]
                
        return result
        
