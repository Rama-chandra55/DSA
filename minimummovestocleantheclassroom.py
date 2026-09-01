class Solution:
    def minMoves(self, classroom: List[str], energy: int) -> int:
        m, n = len(classroom), len(classroom[0])
        litters, start = {}, (0, 0)
        
        # 1. Compact setup for coordinates and bitmask assignment
        for r, row in enumerate(classroom):
            for c, val in enumerate(row):
                if val == 'S': start = (r, c)
                elif val == 'L': litters[(r, c)] = len(litters)
                    
        target_mask = (1 << len(litters)) - 1
        
        # 2. Visited matrix tracks maximum remaining energy for a (row, col, mask) state
        # Utilizing a hash map keeps the memory footprint concise
        visited = {} 
        queue = [(start[0], start[1], 0, energy)]
        moves = 0
        
        # 3. Standard level-by-level BFS iteration loop
        while queue:
            next_queue = []
            for r, c, mask, e in queue:
                if mask == target_mask: 
                    return moves
                if visited.get((r, c, mask), -1) > e: 
                    continue
                
                for dr, dc in ((1,0), (-1,0), (0,1), (0,-1)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < m and 0 <= nc < n and classroom[nr][nc] != 'X' and e > 0:
                        ne, val = e - 1, classroom[nr][nc]
                        nmask = mask | (1 << litters[(nr, nc)]) if val == 'L' else mask
                        ne = energy if val == 'R' else ne
                        
                        # Prune paths that land on 0 energy without picking up all litter or charging
                        if ne == 0 and val != 'R' and nmask != target_mask: 
                            continue
                        
                        if ne > visited.get((nr, nc, nmask), -1):
                            visited[(nr, nc, nmask)] = ne
                            next_queue.append((nr, nc, nmask, ne))
            queue = next_queue
            moves += 1
            
        return -1
