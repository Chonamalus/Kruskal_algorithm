import numpy as np
import random
import raylib


# Class of the underground (no-graphic) maze logic of generation
class MazeGenerator:
    def __init__(self, width_nbrCells, height_nbrCells):
        self.width_nbrCells = width_nbrCells
        self.height_nbrCells = height_nbrCells
        self.visited_cells = np.full((width_nbrCells,height_nbrCells), False, dtype=bool)
        self.path_taken = []
        self.current_cell = (0,0)
        self.previous_cell = None
    
    def generate_step(self): 
        def is_valid(cell): # check wether the case is unvisited and inside the window
            (x,y) = cell
            is_insideWinX = x>=0 and x<self.width_nbrCells
            is_insideWinY = y>=0 and y<self.height_nbrCells
            if is_insideWinX and is_insideWinY:
                is_cellFree = not self.visited_cells[cell]
                is_notPrevious = cell != self.previous_cell
                return is_cellFree and is_notPrevious
            else:
                return False

        def choose_neighbor(cell): # choose a random availible cell
            (x,y) = cell
            neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
            neighbors = [n_cell for n_cell in neighbors if is_valid(n_cell)]
            print("Neighbors:", neighbors)
            return random.choice(neighbors) if len(neighbors)!=0 else None
        
        # Update the attribute of the maze
        theChosenCell = choose_neighbor(self.current_cell)
        print("-> theChosenCell =", theChosenCell)

        if theChosenCell != None: # Build the maze
            # Set the path_taken and visited_cells
            self.path_taken.append(self.current_cell)
            self.visited_cells[self.current_cell] = True
            # Obtain the new path
            self.previous_cell = self.current_cell
            self.current_cell = theChosenCell
            print("==> :) CurPrev Cells:", self.current_cell, self.previous_cell)
            print("==> path_taken:", self.path_taken, "\n")
        else:                      # Backtrack the maze
            self.visited_cells[self.current_cell] = True
            self.previous_cell = self.current_cell
            self.current_cell = self.path_taken.pop()
            print("==> :( CurPrev Cells:", self.current_cell, self.previous_cell)
            print("==> path_taken:", self.path_taken, "\n")

    def is_complete(self):
        return np.all(self.visited_cells == True)


# Draw the graphics of the maze. Outside of the MazeGenerator class
def draw_maze(current_cell, previous_cell, cell_size, wall_thickness):        

    (x_current, y_current) = current_cell
    (x_previous, y_previous) = previous_cell if previous_cell!=None else current_cell

    centerXPrevious = x_previous*cell_size+wall_thickness
    centerYPrevious = y_previous*cell_size+wall_thickness
    centerXCurrent = x_current*cell_size+wall_thickness
    centerYCurrent = y_current*cell_size+wall_thickness

    thicknessXTrace = abs(y_current-y_previous)*(cell_size-2*wall_thickness) + abs(x_current-x_previous)*2*wall_thickness
    thicknessYTrace = abs(x_current-x_previous)*(cell_size-2*wall_thickness) + abs(y_current-y_previous)*2*wall_thickness
    centerXTrace = (centerXPrevious+centerXCurrent+cell_size-2*wall_thickness-thicknessXTrace)//2
    centerYTrace = (centerYPrevious+centerYCurrent+cell_size-2*wall_thickness-thicknessYTrace)//2
    
    raylib.DrawRectangle(   # Draw the previous cell
        centerXPrevious,
        centerYPrevious,
        cell_size-2*wall_thickness,
        cell_size-2*wall_thickness,
        raylib.DARKPURPLE)

    raylib.DrawRectangle(   # Draw the junction between both cells
        centerXTrace,
        centerYTrace,
        thicknessXTrace,
        thicknessYTrace,
        raylib.DARKPURPLE)
    
    raylib.DrawRectangle(   # Draw the current cell
        centerXCurrent,
        centerYCurrent,
        cell_size-2*wall_thickness,
        cell_size-2*wall_thickness,
        raylib.LIME)


# This is the main function
if __name__ == "__main__":
    width_nbrCells = 15 
    height_nbrCells = 10
    maze = MazeGenerator(width_nbrCells, height_nbrCells)

    window_title = "Maze Generator" 
    cell_size = 30
    wall_thickness = 2
    raylib.InitWindow(
        width_nbrCells*cell_size, 
        height_nbrCells*cell_size, 
        window_title.encode("utf-8"))
    raylib.SetTargetFPS(60)
    raylib.ClearBackground(raylib.BLACK)

    generation_complete = False
    while not raylib.WindowShouldClose():
        raylib.BeginDrawing()

        if raylib.IsKeyPressed(raylib.KEY_SPACE):
            if not generation_complete:
                maze.generate_step()
                draw_maze(
                    maze.current_cell, 
                    maze.previous_cell, 
                    cell_size, 
                    wall_thickness)
                if maze.is_complete():
                    generation_complete = True
                    print("Maze is completed !!!")
 
        raylib.EndDrawing()

    raylib.CloseWindow()