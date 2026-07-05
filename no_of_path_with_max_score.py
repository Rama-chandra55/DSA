class Solution:
    def pathsWithMaxScore(self, board):
        MOD = 10**9 + 7
        n = len(board)

        # score[i][j] = maximum score to reach (i, j)
        score = [[-1] * n for _ in range(n)]

        # ways[i][j] = number of ways to reach (i, j)
        ways = [[0] * n for _ in range(n)]

        # Starting from E
        score[0][0] = 0
        ways[0][0] = 1

        for i in range(n):
            for j in range(n):

                if board[i][j] == 'X':
                    continue

                if i == 0 and j == 0:
                    continue

                best = -1
                count = 0

                # From top
                if i > 0 and score[i - 1][j] != -1:
                    if score[i - 1][j] > best:
                        best = score[i - 1][j]
                        count = ways[i - 1][j]
                    elif score[i - 1][j] == best:
                        count = (count + ways[i - 1][j]) % MOD

                # From left
                if j > 0 and score[i][j - 1] != -1:
                    if score[i][j - 1] > best:
                        best = score[i][j - 1]
                        count = ways[i][j - 1]
                    elif score[i][j - 1] == best:
                        count = (count + ways[i][j - 1]) % MOD

                # From diagonal
                if i > 0 and j > 0 and score[i - 1][j - 1] != -1:
                    if score[i - 1][j - 1] > best:
                        best = score[i - 1][j - 1]
                        count = ways[i - 1][j - 1]
                    elif score[i - 1][j - 1] == best:
                        count = (count + ways[i - 1][j - 1]) % MOD

                if best == -1:
                    continue

                # Cell value
                if board[i][j] in ('E', 'S'):
                    value = 0
                else:
                    value = int(board[i][j])

                score[i][j] = best + value
                ways[i][j] = count % MOD

        if ways[n - 1][n - 1] == 0:
            return [0, 0]

        return [score[n - 1][n - 1], ways[n - 1][n - 1]]
