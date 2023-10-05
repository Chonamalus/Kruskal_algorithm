"""
Author : Vincent Badetti for 974BZH group project
Others : Romain Asso & Rachel Neveu
Date : 03/10/23
Title : Maze generator from Kruskal algorithm
This maze generator is wronly written because not optimized for time and space. Also, the final drawing is not a maze because I didn't add the rectangle to make a mark of the track.
"""

import random
import raylib

# This class can be useful to generate a grid using random
class MazeGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[1 for _ in range(width)] for _ in range(height)]
        self.visited = [[False for _ in range(width)] for _ in range(height)]
        self.current_x = 0
        self.current_y = 0
        self.stack = [[0, 0]]  # Change to store lists instead of tuples
        self.previous_positions = []  # Store previous positions

    def generate_step(self):
        def is_valid(x, y):
            return x >= 0 and x < self.width and y >= 0 and y < self.height

        def get_neighbors(x, y):
            neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
            random.shuffle(neighbors)
            return [(nx, ny) for nx, ny in neighbors if is_valid(nx, ny) and not self.visited[ny][nx]]

        if not self.stack:
            return self.grid

        current_position = self.stack[-1]
        x, y = current_position[:2]
        neighbors = get_neighbors(x, y)

        if not neighbors:
            self.stack.pop()
            if self.stack:  # If there are previous positions, store the current position as previous
                self.previous_positions.append(current_position)
            return self.grid

        nx, ny = neighbors[0]
        self.visited[ny][nx] = True
        self.grid[y][x] = 0  # Remove wall
        self.grid[ny][nx] = 0  # Remove wall between current cell and next cell
        self.stack.append([nx, ny])  # Store the new position as a list
        self.current_x, self.current_y = nx, ny

        return self.grid

    def is_complete(self):
        return all(all(row) for row in self.visited)

# Create rectangles of the entire maze
def draw_maze(maze, current_position, previous_positions):
    if maze is None:
        return  # Skip drawing when maze is not available

    cell_size = 30  # Adjust cell size as needed
    wall_thickness = 2  # Adjust wall thickness as needed
    raylib.BeginDrawing()
    raylib.ClearBackground(raylib.BLACK)

    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            cell_x = x * cell_size
            cell_y = y * cell_size
            if [x, y] == current_position[:2]:
                # Draw the current position in LIME
                raylib.DrawRectangle(
                    cell_x + wall_thickness,
                    cell_y + wall_thickness,
                    cell_size - 2 * wall_thickness,
                    cell_size - 2 * wall_thickness,
                    raylib.LIME)
            elif [x, y] in previous_positions:
                # Draw previous positions in BLUE
                raylib.DrawRectangle(
                    cell_x + wall_thickness,
                    cell_y + wall_thickness,
                    cell_size - 2 * wall_thickness,
                    cell_size - 2 * wall_thickness,
                    raylib.BLUE)
            elif cell == 0:  # Create path
                # Draw cell in PURPLE
                raylib.DrawRectangle(
                    cell_x + wall_thickness,
                    cell_y + wall_thickness,
                    cell_size - 2 * wall_thickness,
                    cell_size - 2 * wall_thickness,
                    raylib.DARKPURPLE)

    raylib.EndDrawing()


# The main function
if __name__ == "__main__":
    width = 20  # Adjust the width and height as needed
    height = 10
    generator = MazeGenerator(width, height)

    window_title = "Maze Generator"
    raylib.InitWindow(width * 30, height * 30, window_title.encode("utf-8"))
    raylib.SetTargetFPS(60)

    maze_grid = generator.generate_step()  # Generate the initial cell
    generation_complete = False

    while not raylib.WindowShouldClose():
        if raylib.IsKeyPressed(raylib.KEY_SPACE):
            if not generation_complete:
                maze_grid = generator.generate_step()  # Generate the next cell
                if generator.is_complete():
                    generation_complete = True  # Maze generation is complete

        # Pass the current and previous positions to the draw_maze function, and redraw the entire maze
        draw_maze(maze_grid, generator.stack[-1], generator.previous_positions)

    raylib.CloseWindow()
