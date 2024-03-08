import tkinter as tk
from tkinter import messagebox
from queue import PriorityQueue
import random
from copy import deepcopy
from time import sleep

# Define the size of the puzzle board (N x N)
N = 3

class PuzzleState:
    def __init__(self, board, parent=None, action=None, cost=0):
        self.board = board
        self.parent = parent
        self.action = action
        self.cost = cost
        self.blank_position = self.find_blank()

    def find_blank(self):
        for i in range(N):
            for j in range(N):
                if self.board[i][j] == 0:
                    return i, j

    def successors(self):
        moves = []
        row, col = self.blank_position
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # right, left, down, up

        for d_row, d_col in directions:
            new_row, new_col = row + d_row, col + d_col
            if 0 <= new_row < N and 0 <= new_col < N:
                new_board = deepcopy(self.board)
                new_board[row][col], new_board[new_row][new_col] = new_board[new_row][new_col], new_board[row][col]
                moves.append(PuzzleState(new_board, self, (new_row, new_col), self.cost + 1))

        return moves

    def __lt__(self, other):
        return self.cost < other.cost


def uniform_cost_search(initial_state):
    frontier = PriorityQueue()
    frontier.put(initial_state)
    explored = set()
    step = 0

    while not frontier.empty():
        current_state = frontier.get()
        step += 1
        print(f"Step {step}:")
        for row in current_state.board:
            print(" ".join(map(str, row)))
        print()

        if is_goal_state(current_state):
            return get_solution(current_state)

        explored.add(tuple(map(tuple, current_state.board)))

        for successor in current_state.successors():
            if tuple(map(tuple, successor.board)) not in explored:
                frontier.put(successor)
        
        sleep(1)

    return None


def is_goal_state(state):
    goal_board = [[j + N * i + 1 for j in range(N)] for i in range(N)]
    goal_board[N-1][N-1] = 0
    
    return state.board == goal_board


def get_solution(state):
    solution = []
    while state.parent:
        solution.append(state.action)
        state = state.parent
    return solution[::-1]

class PuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("N-Puzzle Solver")

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.buttons = []
        self.board = []  # Initialize the board attribute

        for i in range(N):
            row_buttons = []
            row_board = []
            for j in range(N):
                button = tk.Button(self.frame, text="", width=2, height=1, command=lambda i=i, j=j: self.move_tile(i, j))
                button.grid(row=i, column=j)
                row_buttons.append(button)
                row_board.append(0)  # Initialize each cell of the board with 0
            self.buttons.append(row_buttons)
            self.board.append(row_board)  # Append the row_board to the board attribute

        self.initialize_board()

    def initialize_board(self):
            # numbers = list(range(N * N))
            # random.shuffle(numbers)  # Shuffle the numbers randomly
            numbers = [1,2,3,4,5,6,7,0,8]
            for i in range(N):
                for j in range(N):
                    self.board[i][j] = numbers[i * N + j]
            self.update_gui()

    def update_gui(self):
        for i in range(N):
            for j in range(N):
                value = self.board[i][j]
                text = str(value) if value != 0 else ""
                self.buttons[i][j].config(text=text)

    def move_tile(self, i, j):
        blank_row, blank_col = self.get_blank_position()
        if (i == blank_row and abs(j - blank_col) == 1) or (j == blank_col and abs(i - blank_row) == 1):
            self.board[blank_row][blank_col], self.board[i][j] = self.board[i][j], self.board[blank_row][blank_col]
            self.update_gui()

    def get_blank_position(self):
        for i in range(N):
            for j in range(N):
                if self.board[i][j] == 0:
                    return i, j

    def solve_puzzle(self):
        initial_state = PuzzleState(self.board)
        solution = uniform_cost_search(initial_state)
        if solution:
            messagebox.showinfo("Solution Found", f"Number of moves: {len(solution)}")
            self.animate_solution(solution)
        else:
            messagebox.showinfo("No Solution", "No solution found for the current puzzle.")
            
    def animate_solution(self, solution):
        step_label = tk.Label(self.root, text="Step: 0")
        step_label.pack()

        for step, action in enumerate(solution, start=1):
            blank_row, blank_col = self.get_blank_position()
            new_row, new_col = blank_row + action[0], blank_col + action[1]
            
            # Ensure the new_row and new_col are within bounds
            if 0 <= new_row < N and 0 <= new_col < N:
                self.board[blank_row][blank_col], self.board[new_row][new_col] = self.board[new_row][new_col], self.board[blank_row][blank_col]
                
                # Update the GUI with the new board configuration
                self.update_gui()
                
                # Update the blank position
                blank_row, blank_col = new_row, new_col
                
                # Update the step label
                step_label.config(text=f"Step: {step}")
            
            self.root.after(500)
            self.root.update_idletasks()


if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleGUI(root)

    solve_button = tk.Button(root, text="Solve", command=app.solve_puzzle)
    solve_button.pack()

    root.mainloop()
