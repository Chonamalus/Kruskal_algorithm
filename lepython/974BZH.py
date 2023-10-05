import random
import raylib

'''
IMPROVEMENT :
Must take care of the fact that there are double in the neighbors list, ex for a 7x7:
[(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (5, 1), !(6, 1), (6, 0), !(6, 1), (6, 2), (6, 3), (6, 4), (5, 4), (5, 3), (5, 2), (4, 2), (3, 2), (2, 2), (2, 1), (2, 2), (1, 2), (1, 3), (0, 3), (0, 4), (1, 4), (2, 4), (2, 5), (2, 6), (3, 6), (3, 5), (3, 4), (4, 4), (4, 5), (5, 5), (5, 6), (5, 5), (6, 5), (4, 5), (4, 4), (4, 3), (3, 3), (3, 6), (2, 6), (1, 6), (0, 6), (0, 5), (1, 6), (2, 5)]
Sometimes it backtracks and keep the old ones, that must have been deleted => found a way to burn them
'''

# Class of the underground (no-graphic) maze logic of generation
class MazeGenerator:
    def __init__(self, width_nbrCells, height_nbrCells):
        self.width_nbrCells = width_nbrCells
        self.height_nbrCells = height_nbrCells
        self.visited_cells = []
        self.current_position = (0,0)
        self.previous_position = None
    
    def generate_step(self):
        def is_valid(x, y): # check wether the case is unvisited and inside the window
            is_insideWinX = x>=0 and x<self.width_nbrCells
            is_insideWinY = y>=0 and y<self.height_nbrCells
            if not self.visited_cells: # no cell visited at all yet
                return is_insideWinX and is_insideWinY
            else:
                is_unvisited = not (x,y) in self.visited_cells
                return is_insideWinX and is_insideWinY and is_unvisited

        def choose_neighbor(position_couple): # choose a random availible cell
            (x,y) = position_couple
            neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
            neighbors = [(nx,ny) for (nx,ny) in neighbors if is_valid(nx,ny)]
            return random.choice(neighbors) if len(neighbors)!=0 else None
        
        # Update the attribute of the maze
        thereIsNoNeighbors = (choose_neighbor(self.current_position) == None)
        print("---", thereIsNoNeighbors)

        if thereIsNoNeighbors: # current_pos becomes previous_pos in visited_cells
            print("[NO NEIGHBORS]", self.current_position, self.previous_position)
            index_prevPosition = self.visited_cells.index(self.previous_position)
            self.previous_position = self.current_position
            self.current_position = self.visited_cells[index_prevPosition -1]
            
        else:   # current_pos becomes the new free cell
            self.previous_position = self.current_position
            self.visited_cells.append(self.current_position)
            self.current_position = choose_neighbor(self.current_position)
            print("[WHERE AM I]", self.current_position, self.previous_position)

    def is_complete(self):
        return len(self.visited_cells) == self.width_nbrCells*self.height_nbrCells


# Draw the graphics of the maze. Outside of the MazeGenerator class
def draw_maze(current_pos, previous_pos, cell_size, wall_thickness):

    (x_current, y_current) = current_pos
    (x_previous, y_previous) = previous_pos if previous_pos!=None else current_pos
    
    raylib.DrawRectangle(   # Draw the previous cell
        x_previous*cell_size+wall_thickness,
        y_previous*cell_size+wall_thickness,
        cell_size-2*wall_thickness,
        cell_size-2*wall_thickness,
        raylib.DARKPURPLE)
    
    raylib.DrawRectangle(   # Draw the junction between both cells
        (x_previous+x_current)*cell_size//2 +wall_thickness,
        (y_previous+y_current)*cell_size//2 +wall_thickness,
        wall_thickness if y_previous==y_current else cell_size-2*wall_thickness,
        wall_thickness if x_previous==x_current else cell_size-2*wall_thickness,
        raylib.WHITE)
    
    raylib.DrawRectangle(   # Draw the current cell
        x_current*cell_size+wall_thickness,
        y_current*cell_size+wall_thickness,
        cell_size-2*wall_thickness,
        cell_size-2*wall_thickness,
        raylib.LIME)


# This is the main function
if __name__ == "__main__":
    width_nbrCells = 7
    height_nbrCells = 7
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
                if maze.is_complete():
                    generation_complete = True
                    print("Maze is completed !!!")
                    print('Visited:',maze.visited_cells)
        draw_maze(
            maze.current_position, 
            maze.previous_position, 
            cell_size, 
            wall_thickness)
 
        raylib.EndDrawing()

    raylib.CloseWindow()
 