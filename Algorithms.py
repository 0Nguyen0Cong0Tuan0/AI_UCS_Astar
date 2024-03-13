from Module import PriorityQueue, psutil, heapq, time

def uniform_cost_search(initial_state, goal_state):
    frontier = PriorityQueue()
    frontier.put(initial_state)
    explored = set()
    step = 0

    max_memory_usage = 0  # Initialize max memory usage
    while not frontier.empty():
        # Check memory usage before expanding node
        memory_usage = get_memory_usage()
        max_memory_usage = max(max_memory_usage, memory_usage)

        current_state = frontier.get()
        step += 1
        print(f"Step {step}:")
        for row in current_state.board:
            print(" ".join(map(str, row)))
        print()

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
    step = 0

    max_memory_usage = 0  # Initialize max memory usage
    while frontier:
        # Check memory usage before expanding node
        memory_usage = get_memory_usage()
        max_memory_usage = max(max_memory_usage, memory_usage)

        current_f_score, current_state = heapq.heappop(frontier)
        step += 1
        print(f"Step {step}:")
        for row in current_state.board:
            print(" ".join(map(str, row)))
        print()

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