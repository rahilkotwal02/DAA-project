import curses
from curses import wrapper
import time
from collections import deque
import sys

# Defined characters for the visualization. These are standard ASCII characters
# to ensure the program runs on any terminal without font issues.
OBSTACLE = "#"
START = "S"
TARGET = "E"
VISITED = "."
FINAL = "*"

# The grid represents our maze.
# '#' is a wall, 'S' is the starting point, 'E' is the target, and ' ' is an open path.
grid = [
    [OBSTACLE, START, OBSTACLE, OBSTACLE, " ", OBSTACLE, OBSTACLE, OBSTACLE, OBSTACLE],
    [OBSTACLE, " ", " ", " ", " ", " ", " ", " ", OBSTACLE],
    [OBSTACLE, " ", OBSTACLE, OBSTACLE, " ", OBSTACLE, OBSTACLE, " ", OBSTACLE],
    [OBSTACLE, " ", OBSTACLE, " ", " ", " ", OBSTACLE, " ", OBSTACLE],
    [OBSTACLE, " ", " ", " ", OBSTACLE, " ", OBSTACLE, " ", OBSTACLE],
    [OBSTACLE, " ", OBSTACLE, " ", OBSTACLE, " ", OBSTACLE, " ", OBSTACLE],
    [OBSTACLE, OBSTACLE, OBSTACLE, " ", OBSTACLE, " ", OBSTACLE, OBSTACLE, OBSTACLE],
    [OBSTACLE, " ", " ", " ", " ", " ", " ", " ", OBSTACLE],
    [OBSTACLE, OBSTACLE, OBSTACLE, OBSTACLE, OBSTACLE, OBSTACLE, OBSTACLE, TARGET, OBSTACLE]
]

# Settings for the visualization, which can be changed in the menu.
animation_speed = 0.5  # Time delay in seconds between each visualization step.
show_stats = True      # A flag to control whether algorithm statistics are displayed.

def safe_addstr(stdscr, y, x, text, color=0):
    """
    A helper function to safely write strings to the curses window.
    It prevents common errors that occur when attempting to write outside
    the terminal's boundaries, making the code more robust.
    """
    max_y, max_x = stdscr.getmaxyx()
    if y >= max_y or x >= max_x or y < 0 or x < 0:
        return
    
    max_len = max_x - x
    if max_len <= 0:
        return
    if len(text) > max_len:
        text = text[:max_len-1]
    
    try:
        stdscr.addstr(y, x, text, color)
    except curses.error:
        pass


def print_grid(stdscr, current_path=[], visited=set(), final_path=[], algorithm=""):
    """
    Renders the current state of the grid to the terminal.
    It highlights the current position, visited cells, and the final path.
    """
    stdscr.clear()
    
    # Predefined color pairs set up in the main menu.
    RED = curses.color_pair(1)
    YELLOW = curses.color_pair(2)
    GREEN = curses.color_pair(3)
    BLUE = curses.color_pair(4)
    
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            symbol = grid[i][j]
            color = 0
            
            # Apply color and symbol changes based on the search state.
            if (i, j) in final_path and final_path:
                symbol = FINAL
                color = GREEN
            elif (i, j) in current_path:
                symbol = START
                color = RED
            elif (i, j) in visited:
                symbol = VISITED
                color = YELLOW
            
            # Using j * 2 for spacing since the characters are single-width.
            safe_addstr(stdscr, i * 2, j * 2, symbol, color)
    
    show_algorithm_guide(stdscr, algorithm, current_path, visited, final_path)


def show_algorithm_guide(stdscr, algorithm, current_path, visited, final_path):
    """
    Displays a legend and a brief explanation of the currently running algorithm.
    This helps the user understand the underlying logic as the visualization runs.
    """
    BLUE = curses.color_pair(4)
    guide_row = len(grid) * 2 + 2
    
    safe_addstr(stdscr, guide_row, 0, "LEGEND:", BLUE)
    safe_addstr(stdscr, guide_row + 1, 0, f"{START} = Current position", curses.color_pair(1))
    safe_addstr(stdscr, guide_row + 2, 0, f"{VISITED} = Already visited", curses.color_pair(2))
    safe_addstr(stdscr, guide_row + 3, 0, f"{FINAL} = Final path", curses.color_pair(3))
    safe_addstr(stdscr, guide_row + 4, 0, f"{OBSTACLE} = Obstacle  {TARGET} = Target", BLUE)
    
    if algorithm == "BFS":
        safe_addstr(stdscr, guide_row + 6, 0, "BFS (Breadth-First Search):", BLUE)
        safe_addstr(stdscr, guide_row + 7, 0, "• Uses a QUEUE (First In, First Out)", BLUE)
        safe_addstr(stdscr, guide_row + 8, 0, "• Explores level by level from the start", BLUE)
        safe_addstr(stdscr, guide_row + 9, 0, "• Guarantees finding the shortest path", BLUE)
        if current_path:
            safe_addstr(stdscr, guide_row + 10, 0, f"Currently exploring all positions at level {len(current_path) - 1} from start.", BLUE)
    
    elif algorithm == "DFS":
        safe_addstr(stdscr, guide_row + 6, 0, "DFS (Depth-First Search):", BLUE)
        safe_addstr(stdscr, guide_row + 7, 0, "• Uses a STACK (Last In, First Out)", BLUE)
        safe_addstr(stdscr, guide_row + 8, 0, "• Goes as deep as possible first, then backtracks", BLUE)
        safe_addstr(stdscr, guide_row + 9, 0, "• The path found may NOT be the shortest", BLUE)
        if current_path:
            safe_addstr(stdscr, guide_row + 10, 0, f"Currently at a depth of {len(current_path) - 1} steps from start.", BLUE)


def show_stats(stdscr, algorithm, steps, visited_count, queue_size=0, path_length=0):
    """
    Displays performance statistics for the running algorithm.
    """
    if not show_stats:
        return
    
    BLUE = curses.color_pair(4)
    stats_row = len(grid) * 2 + 12
    
    safe_addstr(stdscr, stats_row, 0, "STATISTICS:", BLUE)
    safe_addstr(stdscr, stats_row + 1, 0, f"Steps taken: {steps}", BLUE)
    safe_addstr(stdscr, stats_row + 2, 0, f"Positions visited: {visited_count}", BLUE)
    safe_addstr(stdscr, stats_row + 3, 0, f"Queue/Stack size: {queue_size}", BLUE)
    if path_length > 0:
        safe_addstr(stdscr, stats_row + 4, 0, f"Final path length: {path_length}", BLUE)

def show_step_by_step_explanation(stdscr, step_info):
    """
    Provides a more detailed, step-by-step text description of the algorithm's actions.
    """
    BLUE = curses.color_pair(4)
    explain_row = len(grid) * 2 + 17
    
    safe_addstr(stdscr, explain_row, 0, f"STEP {step_info['step']}:", BLUE)
    safe_addstr(stdscr, explain_row + 1, 0, step_info['action'], BLUE)
    safe_addstr(stdscr, explain_row + 2, 0, step_info['reason'], BLUE)

def find_start():
    """Finds and returns the starting position (S) in the grid."""
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == START:
                return (i, j)
    return None

def find_target():
    """Finds and returns the target position (E) in the grid."""
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == TARGET:
                return (i, j)
    return None

def get_neighbors(row, col):
    """
    Generates a list of valid neighboring coordinates (up, down, left, right).
    """
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for dr, dc in directions:
        new_row = row + dr
        new_col = col + dc
        
        if (0 <= new_row < len(grid) and 
            0 <= new_col < len(grid[0])):
            neighbors.append((new_row, new_col))
    
    return neighbors

def is_obstacle(row, col):
    """Checks if a given coordinate is a wall (#)."""
    return grid[row][col] == OBSTACLE

def bfs_search(stdscr):
    """
    The main logic for the Breadth-First Search algorithm.
    It finds the shortest path and provides step-by-step visualization.
    """
    start_pos = find_start()
    target_pos = find_target()
    
    queue = deque([(start_pos, [start_pos])])
    visited = {start_pos}
    steps = 0
    
    while queue:
        current_pos, path = queue.popleft()
        row, col = current_pos
        steps += 1
        
        # Details for the step-by-step explanation.
        step_info = {
            'step': steps,
            'action': f"Exploring position {current_pos} from the front of the queue.",
            'reason': f"BFS explores nodes at the same 'level' before moving deeper (level {len(path) - 1})."
        }
        
        print_grid(stdscr, path, visited, algorithm="BFS")
        show_stats(stdscr, "BFS", steps, len(visited), len(queue))
        show_step_by_step_explanation(stdscr, step_info)
        stdscr.refresh()
        time.sleep(animation_speed)
        
        if current_pos == target_pos:
            # Path found! Show the final path and a success message.
            print_grid(stdscr, [], visited, path, "BFS")
            show_stats(stdscr, "BFS", steps, len(visited), 0, len(path))
            safe_addstr(stdscr, len(grid) * 2 + 20, 0, "🎉 BFS found the SHORTEST path! Press any key...", curses.color_pair(3))
            stdscr.refresh()
            return path
        
        # Explore unvisited neighbors.
        for neighbor in get_neighbors(row, col):
            if neighbor not in visited and not is_obstacle(neighbor[0], neighbor[1]):
                new_path = path + [neighbor]
                queue.append((neighbor, new_path))
                visited.add(neighbor)
    
    # If the queue is empty and the target was not found.
    safe_addstr(stdscr, len(grid) * 2 + 20, 0, "BFS: No path found! Press any key...", curses.color_pair(1))
    stdscr.refresh()
    return None


def dfs_search(stdscr):
    """
    The main logic for the Depth-First Search algorithm.
    It explores deep into a path before backtracking, providing a visualization of this process.
    """
    start_pos = find_start()
    target_pos = find_target()
    
    # DFS uses a stack (LIFO: Last-In, First-Out).
    stack = [(start_pos, [start_pos])]
    visited = set()
    steps = 0
    
    while stack:
        current_pos, path = stack.pop()
        
        if current_pos in visited:
            continue
        
        visited.add(current_pos)
        row, col = current_pos
        steps += 1
        
        # Details for the step-by-step explanation.
        step_info = {
            'step': steps,
            'action': f"Exploring position {current_pos} from the top of the stack.",
            'reason': f"DFS goes as deep as possible first before backtracking (depth {len(path) - 1})."
        }
        
        print_grid(stdscr, path, visited, algorithm="DFS")
        show_stats(stdscr, "DFS", steps, len(visited), len(stack))
        show_step_by_step_explanation(stdscr, step_info)
        stdscr.refresh()
        time.sleep(animation_speed)
        
        if current_pos == target_pos:
            # Path found! Show the final path and a success message.
            print_grid(stdscr, [], visited, path, "DFS")
            show_stats(stdscr, "DFS", steps, len(visited), 0, len(path))
            safe_addstr(stdscr, len(grid) * 2 + 20, 0, "🎉 DFS found a path! (May not be shortest) Press any key...", curses.color_pair(3))
            stdscr.refresh()
            return path
        
        neighbors = get_neighbors(row, col)
        neighbors.reverse()
        
        for neighbor in neighbors:
            if neighbor not in visited and not is_obstacle(neighbor[0], neighbor[1]):
                new_path = path + [neighbor]
                stack.append((neighbor, new_path))
    
    # If the stack is empty and the target was not found.
    safe_addstr(stdscr, len(grid) * 2 + 20, 0, "DFS: No path found! Press any key...", curses.color_pair(1))
    stdscr.refresh()
    return None


def main_menu(stdscr):
    """
    The main menu for the application. It displays options and handles user input
    to run the different algorithms or adjust settings.
    """
    # Setup color pairs for the terminal UI.
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
    
    while True:
        stdscr.clear()
        safe_addstr(stdscr, 2, 5, " PATHFINDING ALGORITHMS TUTORIAL ", curses.color_pair(3))
        safe_addstr(stdscr, 4, 5, "1. BFS - Breadth-First Search", curses.color_pair(4))
        safe_addstr(stdscr, 5, 8, "(Explores level by level, finds shortest path)")
        safe_addstr(stdscr, 6, 5, "2. DFS - Depth-First Search", curses.color_pair(4))
        safe_addstr(stdscr, 7, 8, "(Goes deep first, uses less memory)")
        safe_addstr(stdscr, 8, 5, "3. Settings", curses.color_pair(4))
        safe_addstr(stdscr, 9, 5, "4. Quit", curses.color_pair(4))
        
        safe_addstr(stdscr, 11, 5, " Each algorithm shows step-by-step what it's doing!")
        safe_addstr(stdscr, 13, 5, "Enter choice (1-4): ")
        stdscr.refresh()
        
        choice = stdscr.getch()
        
        if choice == ord('1'):
            stdscr.addstr(0, 0, "Running BFS...")
            stdscr.refresh()
            time.sleep(1)
            bfs_search(stdscr)
            stdscr.getch()
        elif choice == ord('2'):
            stdscr.addstr(0, 0, "Running DFS...")
            stdscr.refresh()
            time.sleep(1)
            dfs_search(stdscr)
            stdscr.getch()
        elif choice == ord('3'):
            settings_menu(stdscr)
        elif choice == ord('4'):
            break


def settings_menu(stdscr):
    """
    A simple settings menu to adjust visualization parameters.
    """
    global animation_speed, show_stats
    
    while True:
        stdscr.clear()
        safe_addstr(stdscr, 2, 5, " SETTINGS ", curses.color_pair(4))
        safe_addstr(stdscr, 4, 5, f"1. Animation Speed: {animation_speed:.1f} seconds")
        safe_addstr(stdscr, 5, 5, "   (How fast the algorithms run)")
        safe_addstr(stdscr, 6, 5, f"2. Show Statistics: {'ON' if show_stats else 'OFF'}")
        safe_addstr(stdscr, 7, 5, "   (Show step counts and details)")
        safe_addstr(stdscr, 9, 5, "3. Back to main menu")
        safe_addstr(stdscr, 11, 5, "Enter choice (1-3): ")
        stdscr.refresh()
        
        choice = stdscr.getch()
        
        if choice == ord('1'):
            safe_addstr(stdscr, 13, 5, "Enter speed (0.1 = fast, 2.0 = slow): ")
            stdscr.refresh()
            curses.echo()
            try:
                speed_input = stdscr.getstr(13, 44, 5).decode('utf-8')
                new_speed = float(speed_input)
                if 0.1 <= new_speed <= 2.0:
                    animation_speed = new_speed
                else:
                    safe_addstr(stdscr, 15, 5, " Please enter between 0.1 and 2.0")
                    stdscr.refresh()
                    time.sleep(1.5)
            except:
                safe_addstr(stdscr, 15, 5, " Invalid input!")
                stdscr.refresh()
                time.sleep(1.5)
            curses.noecho()
        
        elif choice == ord('2'):
            show_stats = not show_stats
        
        elif choice == ord('3'):
            break

def main(stdscr):
    """
    The main entry point of the curses application.
    """
    curses.curs_set(0)  # Hide the cursor for a cleaner look.
    main_menu(stdscr)


if __name__ == "__main__":
    wrapper(main)


# python "R:\DAA-project\bfs-dfs-visualizer\pathfinding_visualizer.py"