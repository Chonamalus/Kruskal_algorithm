# Fonctionnement du code
Le code n'est pas celui de la génération type Kruskal, mais plutot une génération étapes par étapes.
On se place à une case, on choisit un voisin que l'on a pas encore rencontré (unvisited) et on va vers cette case que l'on marque comme visité.

Lorsqu'on se retrouve entouré de cases déja visitées, on (backtrack). On retourne à la case précédente jusqu'à retrouver la case qui nous à fait aller vers le cul-de-sac. Ce qui nous donne la possibilité de retrouver une case (unvisited), qui est à côté de l'entrée au cul-de-sac.

Pour que l'algo puisse terminer, on regarde si toutes les cases ont été visitées.

### Modélisation d'un labyrinthe
```python
def __init__(self, width_nbrCells, height_nbrCells):
    self.width_nbrCells = width_nbrCells
    self.height_nbrCells = height_nbrCells
    self.visited_cells = np.full((width_nbrCells,height_nbrCells), False, dtype=bool)
    self.path_taken = []
    self.current_cell = (0,0)
    self.previous_cell = None
```
On retrouve ici tout les attributs du labyrinthe, qui sont définit par sa dimension initialement.
Le `visited_cells` est une matrice de numpy, qui est de taille fixé et qui représente toutes les cases si elles ont été visitées.
Les `current_cell` et `previous_cell` sont les couples des positions courante et précédente prise sur le chemin emprunté.
Le `path_taken` est une liste qui contiendra les couples des positions prises par le chemin emprunté. Elle est variable, évolue à chaque fois qu'on découvre une case, et diminue lorsqu'on backtrack, car on utilise cette liste pour retrouver notre chemin.

### Choix d'une case voisine
```python
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
```
Ici, cette fonction cherche à vérifié si une case est non-visité et dans le labyrinthe. Si c'est le cas, on la considère valide, autrement on l'a retire.
Si dans cette fonction il y a plusieurs niveaux de `if`, c'est parce qu'on a besoin d'éviter de vérifier la valeur d'une case (visité ou non) si on est hors de la matrice.

```python
def choose_neighbor(cell): # choose a random availible cell
    (x,y) = cell
    neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    neighbors = [n_cell for n_cell in neighbors if is_valid(n_cell)]
    print("Neighbors:", neighbors)
    return random.choice(neighbors) if len(neighbors)!=0 else None
```
A partir d'une case (cell), on regarde ces voisins qui sont juste à côté, et on les filtres avec la fonction précédente. Puis, on retourne seulement l'un d'entre eux au hasard, et si il y en a aucun on retourne `None`.

### Algorithme général
On commence par récupérer le couple de la future case choisie :
```python
theChosenCell = choose_neighbor(self.current_cell) 
```

Si il y a une case non-visité que l'on a chosit, on construit le labyrinthe :
```python
if theChosenCell != None: # Build the maze
    # Set the path_taken and visited_cells
    self.path_taken.append(self.current_cell)
    self.visited_cells[self.current_cell] = True
    # Obtain the new path
    self.previous_cell = self.current_cell
    self.current_cell = theChosenCell
    print("==> :) CurPrev Cells:", self.current_cell, self.previous_cell)
    print("==> path_taken:", self.path_taken, "\n")
```
Ici, dans le `path_taken` on concatène le couple de la `current_cell`, qui va devenir la `previous_cell` après. Puis dans `visited_cells` on marque la case comme visitée. Et à la fin, on modifie la `previous_cell` et la `current_cell`.

Si on ne trouve aucune case non visité, on backtrack :
```python
else:   # Backtrack the maze
    self.visited_cells[self.current_cell] = True
    self.previous_cell = self.current_cell
    self.current_cell = self.path_taken.pop()
    print("==> :( CurPrev Cells:", self.current_cell, self.previous_cell)
    print("==> path_taken:", self.path_taken, "\n")
```
Ici, la première chose qu'on fait est de marqué la case courante comme visité, car on va repartir ce celle-ci. Ensuite, on modifie la `previous_cell` et la `current_cell`, avec la `current_cell` qui récupère la case précédente dans le `path_taken` et retire par la même occasion cette case du `path_taken`. Ainsi, on recule à la case précédente.

### Terminaison

Pour terminer le code, on teste à chaque itération la fonction `is_complete(maze)` :
```python
def is_complete(self):
    return np.all(self.visited_cells == True)
```
Cette fonction traverse chaque case de la matrice `visited_cells` et teste si elles sont toutes `True` donc si elles sont toutes visitées.

### Présentation d'une partie du main
```python
# generation_complete = False (initialy set to False)
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
```


# Commentaire sur les erreurs rencontrées

### Première erreur: le List de List non-mutable!! 
Elle remplaçait toute une colone au lieu de changer juste la case.
Exemple :
```
[[ True  True  True False False False False]
 [ True  True  True False False False False]
 [ True  True  True False False False False]
 [ True  True  True False False False False]
 [ True  True  True False False False False]
 [ True  True  True False False False False]
 [ True  True  True False False False False]]
```
*Solution :* remplacer par un numpy array, qui est mieux fait.


### Seconde erreur: on reste enfermé lors d'un backtrack trop poussé
```
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
```

*Solution :* on backtrack en utilisant la previous cell, lors du test de validité, il faut que les cases qu'on choisit soient différentes de la previous, comme ça on ne retouche pas à celle qu'on a pris juste avant !! Et pas de prise de mémoire trop grande, si le labyrinthe est infini.


### Troisième erreur: le dessin de la trace derrière les nouvelles cells
Le dessin de la trace n'était jamais bien placé et j'ai eu beaucoup de mal à le faire.
Il a été fastidieux de trouver la solution, j'ai du revenir aux bases, faire des schémas, le faire par dichotomie, et recherche longue, mais j'y suis arrivé....

*Solution :* La fonction drawRectangle ne dessine pas le centre du rectangle aux deux premières variables, mais le coin supérieur-gauche, puis dessine le rectangle à partir 


# Commentaire sur les complexitées de l'algorithme
???