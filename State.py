from Module import deepcopy

class PuzzleState:
    def __init__(self, board, parent=None, action=None, cost=0):
        self.board = board
        self.parent = parent
        self.action = action
        self.cost = cost
        self.blank_position = self.find_blank()

    def find_blank(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 0:
                    return i, j

    def successors(self):
        moves = []
        row, col = self.blank_position
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # right, left, down, up

        for d_row, d_col in directions:
            new_row, new_col = row + d_row, col + d_col
            if 0 <= new_row < len(self.board) and 0 <= new_col < len(self.board[0]):
                new_board = deepcopy(self.board)
                new_board[row][col], new_board[new_row][new_col] = new_board[new_row][new_col], new_board[row][col]
                moves.append(PuzzleState(new_board, self, (new_row, new_col), self.cost + 1))

        return moves

    def __lt__(self, other):
        return self.cost < other.cost