#pragma once
#include <iostream>
#include <vector>
#include <raylib.h>

class Maze {
  public:
    Maze(int m_widthNbrCells, int m_heightNbrCells);
    ~Maze();

  private:
    int widthNbrCells, heightNbrCells;
    bool* visitedCells; // 1D array
    std::vector<std::pair<int, int>> pathTaken;
    std::pair<int, int> currentCell;
    std::pair<int, int> previousCell;
}