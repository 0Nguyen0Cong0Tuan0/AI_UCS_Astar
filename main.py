import tkinter as tk
from tkinter import messagebox
from copy import deepcopy
from queue import PriorityQueue
import heapq
import psutil
import time

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
    
def uniform_cost_search(initial_state, goal_state):
    frontier = PriorityQueue()
    frontier.put(initial_state)
    explored = set()

    max_memory_usage = 0  # Initialize max memory usage
    while not frontier.empty():
        # Check memory usage before expanding node
        memory_usage = get_memory_usage()
        max_memory_usage = max(max_memory_usage, memory_usage)

        current_state = frontier.get()

        if current_state.board == goal_state:
            return get_solution(current_state), max_memory_usage

        explored.add(tuple(map(tuple, current_state.board)))

        for successor in current_state.successors():
            if tuple(map(tuple, successor.board)) not in explored:
                frontier.put(successor)

    return None, max_memory_usage

def inversion_distance(state):
    inv_count = 0
    for i in range(len(state.board) * len(state.board[0]) - 1):
        for j in range(i + 1, len(state.board) * len(state.board[0])):
            row1, col1 = divmod(i, len(state.board[0]))
            row2, col2 = divmod(j, len(state.board[0]))
            if state.board[row1][col1] != 0 and state.board[row2][col2] != 0 and state.board[row1][col1] > state.board[row2][col2]:
                inv_count += 1
    return inv_count

def a_star_inversion_distance(initial_state, goal_state):
    frontier = []  # Use a list as a priority queue
    heapq.heappush(frontier, (0, initial_state))  # Add initial state with f-score 0
    explored = set()
    
    max_memory_usage = 0  # Initialize max memory usage
    while frontier:
        # Check memory usage before expanding node
        memory_usage = get_memory_usage()
        max_memory_usage = max(max_memory_usage, memory_usage)

        current_f_score, current_state = heapq.heappop(frontier)

        if current_state.board == goal_state:
            return get_solution(current_state), max_memory_usage

        explored.add(tuple(map(tuple, current_state.board)))

        for successor in current_state.successors():
            if tuple(map(tuple, successor.board)) not in explored:
                g_score = current_state.cost + 1  # Assuming each move has a cost of 1
                h_score = inversion_distance(successor)
                f_score = g_score + h_score
                heapq.heappush(frontier, (f_score, successor))

    return None, max_memory_usage

def get_memory_usage():
    # Get memory usage in bytes
    memory_usage_bytes = psutil.Process().memory_info().rss
    # Convert to MB
    memory_usage_mb = memory_usage_bytes / (1024 * 1024)
    return memory_usage_mb

def get_solution(state):
    solution = []
    while state.parent:
        solution.append(state.action)
        state = state.parent
    return solution[::-1]

def calculate_time(func):
    start_time = time.time()
    solution, memory_usage = func()
    end_time = time.time()
    elapsed_time_ms = (end_time - start_time) * 1000 
    return solution, elapsed_time_ms, memory_usage

class PuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("N-Puzzle Solver")
        self.root.geometry("600x500")  # Adjusted window size
        self.root.configure(bg="#F0F0F0")  # Set background color to slight yellow
        self.sizeFont = 10
        
        self.create_menu()

    def create_menu(self):
        menu_frame = tk.Frame(self.root)
        menu_frame.pack()

        space_label = tk.Label(menu_frame, text="", pady=15)
        space_label.pack()

        input_label = tk.Label(menu_frame, text="INPUT", font=("Helvetica", 16, "bold"), fg="#FF0000", justify="center", padx=100, pady=20)
        input_label.pack()

        size_label = tk.Label(menu_frame, text="Enter the size of the board (N)", font=("Helvetica", 10, "bold"))
        size_label.pack()

        self.size_entry = tk.Entry(menu_frame)
        self.size_entry.pack()

        order_label = tk.Label(menu_frame, text="Enter numbers on the board (comma-separated)\n IF THE BLANK SPACE, PLEASE INPUT 0", font=("Helvetica", 10, "bold"))
        order_label.pack()

        self.order_entry = tk.Entry(menu_frame)
        self.order_entry.pack()

        space_label = tk.Label(menu_frame, text="", pady=5)
        space_label.pack()

        menu_label = tk.Label(menu_frame, text="CHOOSE THE ALGORITHM", font=("Helvetica", 16, "bold"), fg="#FF0000", justify="center", padx=100, pady=20)
        menu_label.pack()

        uniform_cost_button = tk.Button(menu_frame, text="Uniform Cost Search", font=("Helvetica", self.sizeFont, "bold"), command=self.open_puzzle_uniform_cost, padx=10, pady=10)
        uniform_cost_button.pack()

        space_label = tk.Label(menu_frame, text="", pady=5)
        space_label.pack()

        astar_button = tk.Button(menu_frame, text="A* Search", font=("Helvetica", self.sizeFont, "bold"), command=self.open_puzzle_astar, padx=10, pady=10)
        astar_button.pack()

    def open_puzzle_uniform_cost(self):
        size = int(self.size_entry.get())
        order = list(map(int, self.order_entry.get().split(',')))
        self.root.destroy()  # Close the menu window
        root = tk.Tk()
        app = PuzzleInterface(root, "Uniform Cost Search", size, order)
        solve_button = tk.Button(root, text="Solve", command=app.solve_puzzle_uniform_cost)
        solve_button.pack()
        root.mainloop()

    def open_puzzle_astar(self):
        size = int(self.size_entry.get())
        order = list(map(int, self.order_entry.get().split(',')))
        self.root.destroy()  # Close the menu window
        root = tk.Tk()
        app = PuzzleInterface(root, "A* Search", size, order)
        solve_button = tk.Button(root, text="Solve", command=app.solve_puzzle_astar)
        solve_button.pack()
        root.mainloop()

class PuzzleInterface:
    def __init__(self, root, algorithm, size, order):
        self.root = root
        self.root.title("N-Puzzle Solver")
        self.root.geometry("600x500")  # Adjusted window size
        self.root.configure(bg="#FFFFE0")  # Set background color to slight yellow

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.buttons = []
        self.board = []  # Initialize the board attribute
        self.temp_board = []  # Initialize the temp_board attribute
        self.size = size
        self.order = order

        self.goal_board = [[j + size * i + 1 for j in range(size)] for i in range(size)]
        self.goal_board[size-1][size-1] = 0

        for i in range(self.size):
            row_buttons = []
            row_board = []
            row_temp_board = []  # Initialize row for temp_board
            for j in range(self.size):
                button = tk.Button(self.frame, text="", width=2, height=1, command=lambda i=i, j=j: self.move_tile(i, j))
                button.grid(row=i, column=j)
                row_buttons.append(button)
                row_board.append(0) 
                row_temp_board.append(0)  # Add placeholder value to temp_board
            self.buttons.append(row_buttons)
            self.board.append(row_board)
            self.temp_board.append(row_temp_board)  # Append the row to temp_board

        self.initialize_board()

        self.state_display = tk.Text(self.root, height=10, width=30)  # Create a Text widget to display the state
        self.state_display.pack()

        self.algorithm = algorithm

    def initialize_board(self):
        for i in range(self.size):
            for j in range(self.size):
                self.board[i][j] = self.order[i * self.size + j]
                self.temp_board[i][j] = self.order[i * self.size + j]  # Initialize temp_board with the same values as board
        self.update_gui()

    def update_gui(self):
        for i in range(self.size):
            for j in range(self.size):
                value = self.board[i][j]
                text = str(value) if value != 0 else ""
                self.buttons[i][j].config(text=text)

    def move_tile(self, i, j):
        blank_row, blank_col = self.get_blank_position()
        if (i == blank_row and abs(j - blank_col) == 1) or (j == blank_col and abs(i - blank_row) == 1):
            self.board[blank_row][blank_col], self.board[i][j] = self.board[i][j], self.board[blank_row][blank_col]
            self.update_gui()

    def get_blank_position(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    return i, j
                
    def get_blank_position_in_temp(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.temp_board[i][j] == 0:
                    return i, j

    def solve_puzzle_uniform_cost(self):
        initial_state = PuzzleState(self.board)
        solution, elapsed_time, memory_usage = calculate_time(lambda: uniform_cost_search(initial_state, self.goal_board))
        if solution:
            messagebox.showinfo("Solution Found", f"Number of moves: {len(solution)} \nTime taken: {elapsed_time:.4f} ms \nMemory usage: {memory_usage:.4f}MB")
            self.animate_solution(solution, elapsed_time, memory_usage)
            self.display_solution(solution)
        else:
            messagebox.showinfo("No Solution", "No solution found for the current puzzle \n                            OR  \n            Your input is in goal state")

    def solve_puzzle_astar(self):
        initial_state = PuzzleState(self.board)
        solution, elapsed_time, memory_usage = calculate_time(lambda: a_star_inversion_distance(initial_state, self.goal_board))
        if solution:
            messagebox.showinfo("Solution Found", f"Number of moves: {len(solution)} \nTime taken: {elapsed_time:.4f} ms \nMemory usage: {memory_usage:.4f}MB")
            self.animate_solution(solution, elapsed_time, memory_usage)
            self.display_solution(solution)
        else:
            messagebox.showinfo("No Solution", "No solution found for the current puzzle \n                            OR  \n           Your input is in goal state")

    def animate_solution(self, solution, elapsed_time, memory_usage):
        # Update the step label
        step_label = tk.Label(self.root, text=f"Step: {len(solution)}", bg="#FFFFE0")
        step_label.pack()
        time_label = tk.Label(self.root, text=f"Time taken: {elapsed_time:.4f}ms", bg="#FFFFE0")
        time_label.pack()
        memory_label = tk.Label(self.root, text=f"Memory usage: {memory_usage:.4f}MB", bg="#FFFFE0")
        memory_label.pack()

        for step, action in enumerate(solution, start=1):
            blank_row, blank_col = self.get_blank_position()
            new_row, new_col = blank_row + action[0], blank_col + action[1]

            # Ensure the new_row and new_col are within bounds
            if 0 <= new_row < self.size and 0 <= new_col < self.size:
                self.board[blank_row][blank_col], self.board[new_row][new_col] = self.board[new_row][new_col], self.board[blank_row][blank_col]

                # Update the blank position
                blank_row, blank_col = new_row, new_col
                
                self.root.update_idletasks()

    def display_solution(self, solution):
        self.state_display.delete(1.0, tk.END)  # Clear the text widget before displaying the solution

        current_board = deepcopy(self.temp_board) # Create a copy of the initial board
        
        # Insert the initial state of the puzzle
        self.state_display.insert(tk.END, "RESULT\nInitial State:\n")

        for row in current_board:
            for index, element in enumerate(row):
                if element == 0:
                    row[index] = " "

        for row in current_board:
            self.state_display.insert(tk.END, " ".join(map(str, row)) + "\n")
        self.state_display.insert(tk.END, "\n")

        blank_row, blank_col = self.get_blank_position_in_temp()

        for step, action in enumerate(solution, start=1):
            self.state_display.insert(tk.END, f"Step {step}:\n")

            new_row, new_col = action[0], action[1]

            if 0 <= new_row < self.size and 0 <= new_col < self.size:
                current_board[blank_row][blank_col], current_board[new_row][new_col] = current_board[new_row][new_col], current_board[blank_row][blank_col]

                blank_row, blank_col = new_row, new_col 

            for row in current_board:
                self.state_display.insert(tk.END, " ".join(map(str, row)) + "\n")
            self.state_display.insert(tk.END, "\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleGUI(root)

    root.mainloop()