#pragma once
#include <iostream>
#include <raylib.h>

class Cell {
  public:
    Cell();
    ~Cell();

    // void drawCell();
    // void changeCellColor(Color m_cellColor);

  protected:
    // Initialized and fixed attributes
    Color cellColor;
    int cellSize;
    int wallThickness;
    int centerX, centerY;
};