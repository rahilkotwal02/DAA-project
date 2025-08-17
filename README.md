# 🗺 Pathfinding Visualizer (BFS & DFS)

This is a Python-based, terminal-driven tool for visualizing pathfinding algorithms. It uses the curses library to provide an interactive and animated demonstration of *Breadth-First Search (BFS)* and *Depth-First Search (DFS)* on a simple maze.

*Designed as an educational aid for anyone learning about graph traversal algorithms and core data structures like stacks and queues.*

---


## 🎥 Demo

Here is a working demo for BFS & DFS Traversal:

https://github.com/user-attachments/assets/dd25937f-e925-442e-827a-3e9421404cf8


## 🚀 Features

-   *Breadth-First Search (BFS)*: Demonstrates how BFS finds the shortest path by exploring all nodes at the current level before moving to the next.
-   *Depth-First Search (DFS)*: Visualizes how DFS explores as deeply as possible along a single path before backtracking. Note that the path it finds may not be the shortest.
-   *Interactive Menu*: A clean and simple menu allows you to choose which algorithm to run or adjust settings.
-   *Step-by-Step Explanation*: During each run, the visualizer provides a real-time explanation of what the algorithm is doing, helping to reinforce learning.
-   *Customizable Settings*: You can easily change the animation speed to slow down or speed up the visualization and toggle statistics on or off.

---

## 🧰 Tech Stack

-   Python 3.11
-   **curses library**: A standard part of Python for creating terminal-based user interfaces.

---

## 💻 Getting Started

### Prerequisites

-   To run this program, you will need Python 3.11
-   The curses library is required. It's a standard part of Python on most systems.
    -   For *Windows users*, you may need to install it separately:
        
       ```sh

        pip install windows-curses

       ```
        

### Installation

1.  Clone the repository:
    
    ```sh

    git clone https://github.com/rahilkotwal02/DAA-project.git

    ```
2.  Navigate to the project folder:
    
    ```sh

    cd bfs-dfs-visualizer

    ```

---

## ▶ How to Run

1.  Open your terminal or command prompt.
2.  Run the script using the Python interpreter:
    
   ```sh

    python pathfinding_visualizer.py

   ```

3.  The main menu will appear. Use the number keys 1, 2, 3, or 4 to select an option and press Enter, Press Q for Exit.
     You can easily change the animation speed to slow down or speed up the visualization using key 1.

4.  Follow the on-screen prompts to proceed or exit the program.

---

## 📁 Code Structure

The script is a single, self-contained file. Key components include:

-   *Global Constants*: OBSTACLE, START, TARGET, VISITED, and FINAL are defined at the top to make it easy to change the visual characters.
-   main_menu(stdscr): The primary function that sets up color pairs and displays the main user interface.
-   bfs_search(stdscr): The core implementation of the Breadth-First Search algorithm.
-   dfs_search(stdscr): The core implementation of the Depth-First Search algorithm.
-   Helper functions like print_grid() and safe_addstr() for rendering the grid and managing terminal output safely.
-   settings_menu(): A menu for adjusting visualization settings like animation speed.
