#pragma once
#include <iostream>
#include <raylib.h>

class Cell {
  public:
    Cell();
    ~Cell();

    void drawCell(int cellCenterX, int cellCenterY);
    void setCellColor(Color m_cellColor, Color m_cellLineColor);

  private:
    // Initialized and fixed attributes
    Color cellColor;
    Color cellLineColor;
    int cellSize;
    int cellLineWidth; // the line is draw inside of the cell
    // Modifiable attributes
    int cellCenterX, cellCenterY;
};