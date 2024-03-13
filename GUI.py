from Module import tk, deepcopy, messagebox
from State import PuzzleState
from Algorithms import a_star_inversion_distance, uniform_cost_search, calculate_time

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


