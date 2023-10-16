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

        if theChosenCell != None:
            # Set the path_taken and visited_cells
            self.path_taken.append(self.current_cell)
            self.visited_cells[self.current_cell] = True
            # Obtain the new path
            self.previous_cell = self.current_cell
            self.current_cell = theChosenCell
            print("==> :) CurPrev Cells:", self.current_cell, self.previous_cell)
            print("==> path_taken:", self.path_taken, "\n")
        else:
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
    
    raylib.DrawRectangle(   # Draw the previous cell
        x_previous*cell_size+wall_thickness,
        y_previous*cell_size+wall_thickness,
        cell_size-2*wall_thickness,
        cell_size-2*wall_thickness,
        raylib.DARKPURPLE)
    
    centerX = max(x_current,x_previous)*cell_size
    centerY = max(y_current,y_previous)*cell_size

    raylib.DrawRectangle(   # Draw the junction between both cells
        centerX -wall_thickness,
        centerY -wall_thickness,
        2*wall_thickness,
        2*wall_thickness,
        raylib. WHITE)
    
    raylib.DrawRectangle(   # Draw the current cell
        x_current*cell_size+wall_thickness,
        y_current*cell_size+wall_thickness,
        cell_size-2*wall_thickness,
        cell_size-2*wall_thickness,
        raylib.LIME)


# This is the main function
if __name__ == "__main__":
    width_nbrCells = 10 
    height_nbrCells = 5
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


'''
Première erreur: le List de List non-mutable!! 
Qui remplaçait toute une colone au lieu de changer juste la cell!!!
[[ True  True  True False False False False]
 [ True  True  True False False False False]
 [ True  True  True False False False False]
 [ True  True  True False False False False]
 [ True  True  True False False False False]
 [ True  True  True False False False False]
 [ True  True  True False False False False]]

Solution : remplacer par un numpy array, qui est mieux fait
'''

'''
Seconde erreur: on reste enfermé lors d'un backtrack trop poussé
Neighbors: []
-> theChosenCell = None
==> :( CurPrev Cells: (4, 0) (4, 1)

Neighbors: [(4, 1)]
-> theChosenCell = (4, 1)
==> :) CurPrev Cells: (4, 1) (4, 0)

Neighbors: []
-> theChosenCell = None
==> :( CurPrev Cells: (4, 0) (4, 1)

Neighbors: [(4, 1)]
-> theChosenCell = (4, 1)
==> :) CurPrev Cells: (4, 1) (4, 0)

Solution: on backtrack en utilisant la previous cell, lors du test de validité, il faut que les cells qu'on choisit soient différentes de la previous, comme ça on ne retouche pas à celle qu'on a pris juste avant !! Et pas de prise de mémoire trop grande, si le labirhynte est infini
'''

'''
Troisième erreur: le dessin de la trace derrière les nouvelles cells
Le dessin n'était jamais bien placé et j'ai eu beaucoup de mal à le faire.
Solution: la fonction drawRectangle ne met pas le centre aux deux premières variables, mais le coin haut-gauche
'''