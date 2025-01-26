import heapq
import pygame
import numpy as np

def astar_search(maze, start, goal): 
    def heuristic(a, b):  
        return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Calculate the distance between two points a and b

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] 
    open_set = [] 
    heapq.heappush(open_set, (0, start))  # Add the starting cell with a priority of 0
    came_from = {}  # Dictionary to reconstruct the path after reaching the goal
    g_score = {start: 0}  # Track the cost of the shortest path to each cell
    f_score = {start: heuristic(start, goal)}  # Estimated total cost from start to goal

    while open_set:  # Searching while there are cells to explore
        _, current = heapq.heappop(open_set) 
        if current == goal:  # If the goal is reached, reconstruct and return the path
            path = [] 
            while current in came_from:  # Trace back the path from the goal to the start
                path.append(current)  
                current = came_from[current] 
            path.append(start)  
            return path[::-1]  # Reverse the path to get it from start to goal

        for direction in directions:  # Explore all possible movement directions.
            neighbor = (current[0] + direction[0], current[1] + direction[1]) 
            if 0 <= neighbor[0] < len(maze) and 0 <= neighbor[1] < len(maze[0]): 
                if maze[neighbor[0]][neighbor[1]] == 1:  # Skip if the neighbor is a wall (value 1)
                    continue
                tentative_g_score = g_score[current] + 1  
                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current 
                    g_score[neighbor] = tentative_g_score  
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal) 
                    if neighbor not in [i[1] for i in open_set]:  # Add the neighbor to the open set if not already present
                        heapq.heappush(open_set, (f_score[neighbor], neighbor)) 

    return []  # Return an empty list if no path is found.

def display_maze_pygame(maze, path=None, start=None, goal=None, cell_size=30):
    pygame.init()
    height, width = len(maze), len(maze[0])
    screen = pygame.display.set_mode((width * cell_size, height * cell_size))
    pygame.display.set_caption("Maze Display")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Exits the maze display when "X" button is clicked
                running = False

        screen.fill((255, 255, 255))
        for y in range(height):
            for x in range(width):
                rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size) # Drawing the maze grid
                if maze[y][x] == 1:
                    pygame.draw.rect(screen, (0, 0, 0), rect)  # Black for walls
                elif path and (y, x) in path:
                    pygame.draw.rect(screen, (0, 255, 0), rect)  # Green for path
                elif (y, x) == start:
                    pygame.draw.rect(screen, (0, 0, 255), rect)  # Blue for start
                elif (y, x) == goal:
                    pygame.draw.rect(screen, (255, 0, 0), rect)  # Red for goal
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Grid lines

        pygame.display.flip()

    pygame.quit()

def create_maze_pygame():
    pygame.init()
    width = int(input("Enter the width of the maze (in cells): ")) # Sets maze width
    height = int(input("Enter the height of the maze (in cells): ")) # Sets maze height
    cell_size = 30 # Sets the size of one cell
    screen_width = width * cell_size
    screen_height = height * cell_size
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Maze Editor")
    maze = [[0 for _ in range(width)] for _ in range(height)]
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Exits the maze creation when "X" button is clicked
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN: # Makes clicking a cell a wall
                x, y = pygame.mouse.get_pos()
                grid_x = x // cell_size
                grid_y = y // cell_size
                maze[grid_y][grid_x] = 1 - maze[grid_y][grid_x] # Sets cell in maze as a wall
        screen.fill((255, 255, 255))
        for y in range(height):
            for x in range(width):
                rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
                if maze[y][x] == 1: # Draws the cell black if its filled
                    pygame.draw.rect(screen, (0, 0, 0), rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1) # Draws cell borders
        pygame.display.flip() # Updates the display
    pygame.quit()
    return maze

maze = create_maze_pygame()
start_row = int(input("Enter start row: "))
start_col = int(input("Enter start column: "))
goal_row = int(input("Enter goal row: "))
goal_col = int(input("Enter goal column: "))
start = (start_row, start_col) # Sets start cell
goal = (goal_row, goal_col) # Sets end cell
path = astar_search(maze, start, goal)
if path:
    print("Shortest path:", path)
    display_maze_pygame(maze, path, start, goal)
else:
    print("No path found.")
    display_maze_pygame(maze, path=None, start=start, goal=goal)
