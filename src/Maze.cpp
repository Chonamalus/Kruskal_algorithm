#include "Maze.h"

Maze::Maze(int m_widthNbrCells, int m_heightNbrCells) {
    std::cout << "Creation of the Maze" << std::endl;
    currentCell = {0, 0};
}

// Get the values from parameters.h
const int Maze::widthNbrCells = widthNbrCells;
const int Maze::heightNbrCells = heightNbrCells;

Maze::~Maze() { std::cout << "Destruction of a Maze" << std::endl; }
